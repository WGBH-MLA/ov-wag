"""Tests for logging in to Wagtail through Authentik (OpenID Connect)."""

import copy
import importlib
import json
import os
import time
from contextlib import ExitStack, contextmanager
from unittest.mock import patch
from urllib.parse import parse_qs, urlparse

import jwt
from allauth.account.models import EmailAddress
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from requests import Response

import ov_wag.settings.base as base_settings

ISSUER = 'https://auth.example.test/application/o/openvault/'
CLIENT_ID = 'openvault'
LOGIN_URL = '/accounts/oidc/authentik/login/?process=login'
CALLBACK_URL = '/accounts/oidc/authentik/login/callback/'
DISCOVERY_URL = ISSUER + '.well-known/openid-configuration'

DISCOVERY = {
    'issuer': ISSUER,
    'authorization_endpoint': 'https://auth.example.test/application/o/authorize/',
    'token_endpoint': 'https://auth.example.test/application/o/token/',
    'userinfo_endpoint': 'https://auth.example.test/application/o/userinfo/',
    'jwks_uri': ISSUER + 'jwks/',
    'token_endpoint_auth_methods_supported': [
        'client_secret_post',
        'client_secret_basic',
    ],
}


def json_response(data):
    response = Response()
    response.status_code = 200
    response.headers['content-type'] = 'application/json'
    response.encoding = 'utf-8'
    response._content = json.dumps(data).encode()
    return response


class FakeAuthentik:
    """Stands in for the requests session allauth uses to talk to Authentik."""

    def __init__(self, userinfo):
        self.userinfo = userinfo
        self.calls = []

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def get(self, url, **kwargs):
        return self.request('GET', url, **kwargs)

    def request(self, method, url, **kwargs):
        self.calls.append((method, url))
        if url == DISCOVERY_URL:
            return json_response(DISCOVERY)
        if url == DISCOVERY['token_endpoint']:
            now = int(time.time())
            id_token = jwt.encode(
                {
                    'iss': ISSUER,
                    'aud': CLIENT_ID,
                    'sub': self.userinfo['sub'],
                    'iat': now,
                    'exp': now + 600,
                },
                'x' * 32,
                algorithm='HS256',
                headers={'kid': 'test'},
            )
            return json_response(
                {
                    'access_token': 'access-token',
                    'token_type': 'Bearer',
                    'expires_in': 3600,
                    'id_token': id_token,
                }
            )
        if url == DISCOVERY['userinfo_endpoint']:
            return json_response(self.userinfo)
        raise AssertionError(f'Unexpected request to {method} {url}')


@contextmanager
def env_provider_settings():
    """SOCIALACCOUNT_PROVIDERS as built from the env vars the deployment sets."""
    env = {
        'OIDC_SERVER_URL': ISSUER,
        'OIDC_CLIENT_ID': CLIENT_ID,
        'OIDC_CLIENT_SECRET': 'client-secret',
    }
    try:
        with patch.dict(os.environ, env):
            yield copy.deepcopy(importlib.reload(base_settings).SOCIALACCOUNT_PROVIDERS)
    finally:
        importlib.reload(base_settings)


class AuthentikLoginTests(TestCase):
    def setUp(self):
        stack = ExitStack()
        self.addCleanup(stack.close)
        providers = stack.enter_context(env_provider_settings())
        stack.enter_context(override_settings(SOCIALACCOUNT_PROVIDERS=providers))

    def sign_in(self, **userinfo):
        """Run the full authorization code flow against the fake Authentik."""
        userinfo = {
            'sub': 'authentik-user-1',
            'email': 'editor@example.test',
            'email_verified': True,
            'preferred_username': 'editor',
            **userinfo,
        }
        authentik = FakeAuthentik(userinfo)
        with patch.object(
            DefaultSocialAccountAdapter, 'get_requests_session', lambda _: authentik
        ):
            start = self.client.post(LOGIN_URL)
            query = parse_qs(urlparse(start['Location']).query)
            callback = self.client.get(
                CALLBACK_URL, {'code': 'auth-code', 'state': query['state'][0]}
            )
        return start, authentik, callback

    def test_admin_login_page_offers_authentik(self):
        response = self.client.get('/admin/login/')

        self.assertContains(response, f'action="{LOGIN_URL}"')
        self.assertContains(response, 'Sign in with Authentik')

    def test_login_redirects_to_authentik_with_pkce(self):
        start, authentik, _ = self.sign_in()
        location = urlparse(start['Location'])
        query = parse_qs(location.query)

        self.assertEqual(
            f'{location.scheme}://{location.netloc}{location.path}',
            DISCOVERY['authorization_endpoint'],
        )
        self.assertEqual(query['client_id'], [CLIENT_ID])
        self.assertEqual(query['code_challenge_method'], ['S256'])
        self.assertTrue(query['redirect_uri'][0].endswith(CALLBACK_URL))
        # The trailing slash on OIDC_SERVER_URL must not leak into the URL
        self.assertIn(('GET', DISCOVERY_URL), authentik.calls)

    def test_new_user_is_created(self):
        _, _, callback = self.sign_in()

        self.assertEqual(callback.status_code, 302)
        user = get_user_model().objects.get(email='editor@example.test')
        self.assertEqual(self.client.session['_auth_user_id'], str(user.pk))
        self.assertEqual(user.socialaccount_set.get().uid, 'authentik-user-1')

    def test_existing_user_is_linked_by_verified_email(self):
        users = get_user_model().objects
        user = users.create_user(
            'old-auth0-user', 'editor@example.test', 'local-password'
        )
        EmailAddress.objects.create(user=user, email=user.email, verified=True)

        self.sign_in()

        self.assertEqual(users.count(), 1)
        self.assertEqual(self.client.session['_auth_user_id'], str(user.pk))
        self.assertEqual(user.socialaccount_set.get().uid, 'authentik-user-1')
        user.refresh_from_db()
        self.assertTrue(user.has_usable_password())

    def test_unverified_email_does_not_take_over_existing_user(self):
        user = get_user_model().objects.create_user(
            'someone', 'editor@example.test', 'pw'
        )

        self.sign_in(email_verified=False)

        self.assertNotEqual(self.client.session.get('_auth_user_id'), str(user.pk))
        self.assertFalse(user.socialaccount_set.exists())
