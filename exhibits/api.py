from wagtail.api.v2.views import PagesAPIViewSet

from .models import ExhibitPage


class FeaturedExhibitsAPIViewSet(PagesAPIViewSet):
    """API endpoint for featured exhibits"""

    def get_queryset(self):
        return ExhibitPage.objects.live().public().filter(featured=True)
