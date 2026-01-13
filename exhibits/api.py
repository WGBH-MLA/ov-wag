from typing import ClassVar

from wagtail.api.v2.views import PagesAPIViewSet

from .models import OpenVaultExhibit


class ExhibitsAPIViewSet(PagesAPIViewSet):
    model = OpenVaultExhibit

    meta_fields: ClassVar[list[str]] = [
        *PagesAPIViewSet.meta_fields,
        'last_published_at',
        'featured',
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
        'featured',
    ]

    def get_queryset(self):
        """Sort by featured, then most recent last_published_at"""
        return self.model.objects.live().order_by('-featured', '-last_published_at')
