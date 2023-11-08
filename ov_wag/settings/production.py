from contextlib import suppress
from os import environ as env

from ov_wag.settings.base import *  # noqa F403

DEBUG = bool(env.get('OV_DEBUG', False))

SECRET_KEY = env.get('OV_SECRET_KEY')

ALLOWED_HOSTS = env.get('OV_ALLOWED_HOSTS').split(',')

CSRF_TRUSTED_ORIGINS = env.get('OV_TRUSTED_ORIGINS').split(',')
CSRF_COOKIE_SECURE = bool(env.get('OV_CSRF_COOKIE_SECURE', True))
SESSION_COOKIE_SECURE = bool(env.get('OV_SESSION_COOKIE_SECURE', True))
SECURE_SSL_REDIRECT = False

INSTALLED_APPS += [  # noqa: F405
    'storages',
]
# S3 Storage
AWS_STORAGE_BUCKET_NAME = env.get('OV_AWS_STORAGE_BUCKET_NAME')
AWS_ACCESS_KEY_ID = env.get('OV_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env.get('OV_AWS_SECRET_ACCESS_KEY')
AWS_S3_CUSTOM_DOMAIN = f's3.amazonaws.com/{AWS_STORAGE_BUCKET_NAME}'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_S3_FILE_OVERWRITE = False
AWS_S3_SIGNATURE_VERSION = 's3v4'

with suppress(ImportError):
    from .local import *  # noqa F403
