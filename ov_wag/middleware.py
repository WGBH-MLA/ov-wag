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
        # Get the hostname from the request
        hostname = request.host.name

        # Try exact match first (most efficient)
        site = Site.objects.filter(hostname=hostname).first()

        if not site:
            site = Site.objects.filter(is_default_site=True).first()

        if site:
            # Set the site on the request so Wagtail uses it
            request.site = site
            # Also set _wagtail_site for compatibility
            request._wagtail_site = site

        response = self.get_response(request)
        return response
