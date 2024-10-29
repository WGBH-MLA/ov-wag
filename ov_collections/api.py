from typing import ClassVar

from wagtail.api.v2.views import PagesAPIViewSet

from .models import Collection


class CollectionAPIViewSet(PagesAPIViewSet):
    model = Collection

    meta_fields: ClassVar[list[str]] = PagesAPIViewSet.meta_fields + [
        'last_published_at',
    ]

    listing_default_fields: ClassVar[list[str]] = [
        *PagesAPIViewSet.listing_default_fields,
        'title',
        'introduction',
        'cover_image',
        'hero_image',
        'last_published_at',
    ]

    def get_queryset(self):
        return self.model.objects.live().order_by("-last_published_at")
