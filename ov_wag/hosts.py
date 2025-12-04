"""
Django-hosts configuration for Open Vault multi-tenancy.

This module configures host-based routing for OV and AAPB sites.
The DjangoHostsSiteMiddleware (in middleware.py) uses these patterns
to set the correct Wagtail Site on each request.

Environment Variables:
    AAPB_HOST_PATTERN: Regex pattern for AAPB hostnames (default: r'aapb(.+)*')
                       Examples: 'aapb.wgbh.org', 'aapb-staging.wgbh.org'

    OV_HOST_PATTERN: Regex pattern for OV hostnames (default: r'.*')
                     Matches all non-AAPB hostnames

    DEFAULT_HOST: Default host name when pattern doesn't match (default: 'ov')

Usage:
    Set at deployment time via environment variables:
    export AAPB_HOST_PATTERN='aapb\.production\.org'
    export OV_HOST_PATTERN='openvault\.production\.org'
"""

from os import environ as env
from django_hosts import patterns, host
from django.conf import settings

# Get hostname patterns from environment variables
# Note: django-hosts uses Python's re.match() which matches from the start of the string
aapb_pattern = env.get('AAPB_HOST_PATTERN', r'aapb(.+)*')
ov_pattern = env.get('OV_HOST_PATTERN', r'ov(.+)*')

host_patterns = patterns(
    '',
    # Match any hostname starting with 'aapb' (e.g., aapb.wgbh.org, aapb-staging.org)
    host(aapb_pattern, 'ov_wag.urls', name='aapb'),
    # Match everything else (empty pattern matches all)
    host(ov_pattern, 'ov_wag.urls', name='ov'),
)
