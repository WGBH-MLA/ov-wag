from .base import *
from os import environ

DEBUG = False
ALLOWED_HOSTS = os.environ.get('OV_ALLOWED_HOSTS').split(',')
WAGTAIL_BASE_URL = os.environ.get('OV_BASE_URL')

SECRET_KEY = os.environ.get('OV_SECRET_KEY')

try:
    from .local import *
except ImportError:
    pass
