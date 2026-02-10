from contextlib import suppress
from os import environ as env

from ov_wag.settings.base import *  # noqa F403
from ov_wag.utils import environ_bool

DEBUG = environ_bool('OV_DEBUG', False)

SECRET_KEY = env.get('OV_SECRET_KEY')

ALLOWED_HOSTS = env.get('OV_ALLOWED_HOSTS').split(',')

CSRF_TRUSTED_ORIGINS = env.get('OV_TRUSTED_ORIGINS').split(',')
CSRF_COOKIE_SECURE = environ_bool('OV_CSRF_COOKIE_SECURE', True)
SESSION_COOKIE_SECURE = environ_bool('OV_SESSION_COOKIE_SECURE', True)
SECURE_SSL_REDIRECT = False

INSTALLED_APPS += [  # noqa: F405
    'storages',
]

# S3 Storage
AWS_STORAGE_BUCKET_NAME = env.get('AWS_STORAGE_BUCKET_NAME')
AWS_ACCESS_KEY_ID = env.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env.get('AWS_SECRET_ACCESS_KEY')
AWS_S3_FILE_OVERWRITE = False
AWS_S3_REGION_NAME = env.get('AWS_S3_REGION_NAME', 'us-east-1')

STORAGES = {
    'default': {
        'BACKEND': 'storages.backends.s3.S3Storage',
        'OPTIONS': {},
    },
    'staticfiles': {
        'BACKEND': 'storages.backends.s3.S3Storage',
        'OPTIONS': {
            'location': 'static',
            'querystring_auth': False,
            'default_acl': 'public-read',
        },
    },
}

with suppress(ImportError):
    from .local import *  # noqa F403
