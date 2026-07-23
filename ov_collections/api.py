from typing import ClassVar

from wagtail.api.v2.views import PagesAPIViewSet

from aapb_collections.models import AAPBCollection
from tags.filters import TagFilter

from .models import BaseCollection, OpenVaultCollection


class CollectionsAPIViewSet(PagesAPIViewSet):
    model = BaseCollection

    # Enable ?tag=<slug or name> filtering (SearchFilter must stay last).
    filter_backends: ClassVar[list] = [
        *PagesAPIViewSet.filter_backends[:-1],
        TagFilter,
        *PagesAPIViewSet.filter_backends[-1:],
    ]

    known_query_parameters = PagesAPIViewSet.known_query_parameters.union(['tag'])

    meta_fields: ClassVar[list[str]] = [
        *PagesAPIViewSet.meta_fields,
        'last_published_at',
        'featured',
    ]

    listing_default_fields: ClassVar[list[str]] = [
        *PagesAPIViewSet.listing_default_fields,
        'introduction',
        'cover_image',
        'cover_thumb',
        'hero_image',
        'last_published_at',
        'featured',
        'tags',
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
