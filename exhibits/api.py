from typing import ClassVar

from wagtail.api.v2.views import PagesAPIViewSet

from .models import ExhibitPage


class FeaturedExhibitsAPIViewSet(PagesAPIViewSet):
    """API endpoint for featured exhibits"""

    def get_queryset(self):
        return ExhibitPage.objects.live().public().filter(featured=True)


class ExhibitsAPIViewSet(PagesAPIViewSet):
    model = ExhibitPage

    meta_fields: ClassVar[list[str]] = PagesAPIViewSet.meta_fields + [
        'last_published_at',
    ]

    listing_default_fields: ClassVar[list[str]] = [
        *PagesAPIViewSet.listing_default_fields,
        'title',
        'last_published_at',
        'cover_image',
        'cover_thumb',
        'hero_image',
        'hero_thumb',
        'authors',
    ]

    def get_queryset(self):
        return self.model.objects.live().order_by("-last_published_at")
