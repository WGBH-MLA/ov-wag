from contextlib import suppress
from os import environ as env

from ov_wag.settings.base import *  # noqa F403

DEBUG = False

SECRET_KEY = env.get('OV_SECRET_KEY')

ALLOWED_HOSTS = env.get('OV_ALLOWED_HOSTS').split(',')

CSRF_TRUSTED_ORIGINS = env.get('OV_TRUSTED_ORIGINS').split(',')
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = False


with suppress(ImportError):
    from .local import *  # noqa F403
