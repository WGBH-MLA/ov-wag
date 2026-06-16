from typing import ClassVar

from wagtail.api.v2.views import PagesAPIViewSet

from aapb_collections.models import AAPBCollection

from .models import BaseCollection, OpenVaultCollection


class OpenVaultCollectionAPIViewSet(PagesAPIViewSet):
    model = BaseCollection

    meta_fields: ClassVar[list[str]] = [
        *PagesAPIViewSet.meta_fields,
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
        """Return live collections for the current site.

        For the ``aapb`` site, return only ``AAPBCollection`` pages; otherwise
        return only ``OpenVaultCollection`` pages. Sorted by featured, then most
        recent ``last_published_at``.
        """
        host = getattr(self.request, 'host', None)
        if host is not None and host.name == 'aapb':
            model = AAPBCollection
        else:
            model = OpenVaultCollection
        return model.objects.live().order_by('-featured', '-last_published_at')
