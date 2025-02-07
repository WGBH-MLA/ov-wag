from typing import ClassVar

from wagtail.api.v2.views import PagesAPIViewSet

from .models import Collection


class CollectionAPIViewSet(PagesAPIViewSet):
    model = Collection

    meta_fields: ClassVar[list[str]] = PagesAPIViewSet.meta_fields + [
        'last_published_at',
        'featured',
    ]

    listing_default_fields: ClassVar[list[str]] = [
        *PagesAPIViewSet.listing_default_fields,
        'title',
        'introduction',
        'cover_image',
        'hero_image',
        'last_published_at',
        'featured',
    ]

    def get_queryset(self):
        """Sort by featured, then most recent last_published_at"""
        return self.model.objects.live().order_by('-featured', '-last_published_at')
