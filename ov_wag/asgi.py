"""
ASGI config for ov-wag project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

from os import environ

from django.core.wsgi import get_asgi_application

environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    environ.get('DJANGO_SETTINGS_MODULE', 'ov_wag.settings.dev'),
)

application = get_asgi_application()
