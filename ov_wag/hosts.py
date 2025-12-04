from os import environ as env
from django_hosts import patterns, host
from django.conf import settings

host_patterns = patterns(
    '',
    host(r'aapb(.+)*', 'ov_wag.urls', name='aapb'),
    host(r'.*', 'ov_wag.urls', name='ov'),
)
