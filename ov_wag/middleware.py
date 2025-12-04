"""
Custom middleware for Open Vault project.
"""

from django.conf import settings
from wagtail.models import Site


class DjangoHostsSiteMiddleware:
    """
    Middleware that sets the correct Wagtail Site based on django-hosts routing.

    This allows Wagtail to automatically filter pages and content by site without
    needing custom filtering in each API viewset or view.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the host match from django-hosts middleware
        host = getattr(request, 'host', None)

        if host:
            # Determine which site to use based on the host name
            if host.name == 'aapb':
                # Look up AAPB site by root page type
                site = Site.objects.filter(
                    root_page__content_type__model='aapbhomepage'
                ).first()
            else:
                # Look up OV site by root page type
                site = Site.objects.filter(
                    root_page__content_type__model='openvaulthomepage'
                ).first()

            if site:
                # Set the site on the request so Wagtail uses it
                request.site = site
                # Also set _wagtail_site for compatibility
                request._wagtail_site = site

        response = self.get_response(request)
        return response
