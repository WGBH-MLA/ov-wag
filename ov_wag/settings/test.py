from contextlib import suppress

from ov_wag.settings.base import *  # noqa F403

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-qsu^g!8&aye$7b@ucxwa6!**1y@&1uwzcf+rs0832)t-yp7zsp'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

WAGTAILSEARCH_BACKENDS = {'default': {'BACKEND': 'wagtail.search.backends.database'}}

with suppress(ImportError):
    from .local import *  # noqa F403
