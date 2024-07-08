from typing import ClassVar

from wagtail.api.v2.views import PagesAPIViewSet

from .models import ExhibitPage


class ExhibitsAPIViewSet(PagesAPIViewSet):
    model = ExhibitPage

    listing_default_fields: ClassVar[list[str]] = [
        *PagesAPIViewSet.listing_default_fields,
        'title',
        'cover_image',
        'cover_thumb',
        'hero_image',
        'hero_thumb',
        'authors',
    ]

    def get_queryset(self):
        return self.model.objects.live().order_by("-last_published_at")
