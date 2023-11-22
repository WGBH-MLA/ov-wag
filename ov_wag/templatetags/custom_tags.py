from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def get_setting(name):
    return getattr(settings, name, "")


@register.simple_tag
def callback_url():
    return settings.LOGIN_CALLBACK_URL
