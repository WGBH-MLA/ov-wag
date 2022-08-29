"""
WSGI config for ov-wag project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

from os import environ

from django.core.wsgi import get_wsgi_application

environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    environ.get('DJANGO_SETTINGS_MODULE', 'ov_wag.settings.dev'),
)

application = get_wsgi_application()
