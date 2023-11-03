from ov_wag.settings.base import *

DEBUG = False

SECRET_KEY = os.environ.get('OV_SECRET_KEY')

ALLOWED_HOSTS = os.environ.get('OV_ALLOWED_HOSTS').split(',')

CSRF_TRUSTED_ORIGINS = os.environ.get('OV_TRUSTED_ORIGINS').split(',')
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = False

try:
    from .local import *
except ImportError:
    pass
