import logging

from allauth.account.signals import user_logged_in
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

logger = logging.getLogger(__name__)

PROVIDER_ID = 'authentik'


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    """Also links an existing user whose stored email differs only in case.

    allauth lowercases the address it looks up but compares it exactly, so it misses
    users whose email was typed with capitals and would create a second account.
    """

    def authenticate_by_email(self, sociallogin):
        found = super().authenticate_by_email(sociallogin)
        if found:
            return found
        for address in sociallogin.email_addresses:
            if not address.verified:
                continue
            if not self.can_authenticate_by_email(sociallogin, address.email):
                continue
            users = get_user_model().objects.filter(email__iexact=address.email)[:2]
            # Never guess between accounts
            if len(users) == 1:
                return users[0], address.email
        return None


def claimed_groups(sociallogin):
    """Authentik group names from the userinfo response, or the ID token without one."""
    extra_data = sociallogin.account.extra_data or {}
    claims = extra_data.get('userinfo') or extra_data.get('id_token') or {}
    return set(claims.get('groups') or [])


def grant_wagtail_access(sender, user, sociallogin=None, **kwargs):
    """Give Wagtail access to users who sign in through Authentik groups.

    Only grants access: leaving an Authentik group does not remove access that was
    granted here or by hand, but it does stop the user from signing in at all.
    """
    if sociallogin is None or sociallogin.account.provider != PROVIDER_ID:
        return

    groups = claimed_groups(sociallogin)

    is_admin = settings.OIDC_ADMIN_GROUP in groups
    if is_admin and not (user.is_superuser and user.is_staff):
        user.is_superuser = True
        user.is_staff = True
        user.save(update_fields=['is_superuser', 'is_staff'])

    if settings.OIDC_EDITOR_GROUP in groups:
        editors = Group.objects.filter(name=settings.OIDC_WAGTAIL_EDITOR_GROUP).first()
        if editors:
            user.groups.add(editors)
        else:
            logger.warning(
                'Wagtail group %r does not exist, so %s was not given editor access',
                settings.OIDC_WAGTAIL_EDITOR_GROUP,
                user,
            )


def connect_signals():
    user_logged_in.connect(
        grant_wagtail_access, dispatch_uid='ov_wag.auth.grant_wagtail_access'
    )
