from .base import *
from os import environ

DEBUG = False

SECRET_KEY = os.environ.get('OV_SECRET_KEY')

ALLOWED_HOSTS = os.environ.get('OV_ALLOWED_HOSTS').split(',')
WAGTAIL_BASE_URL = os.environ.get('OV_BASE_URL')
WAGTAILADMIN_BASE_URL = os.environ.get('OV_ADMIN_BASE_URL')

CSRF_TRUSTED_ORIGINS = os.environ.get('OV_TRUSTED_ORIGINS').split(',')
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = False

try:
    from .local import *
except ImportError:
    pass
