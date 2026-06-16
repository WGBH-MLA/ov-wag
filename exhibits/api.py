from typing import ClassVar

from wagtail.api.v2.views import PagesAPIViewSet

from aapb_exhibits.models import AAPBExhibit

from .models import BaseExhibitPage, OpenVaultExhibit


class ExhibitsAPIViewSet(PagesAPIViewSet):
    model = BaseExhibitPage

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
        """Return live exhibits for the current site.

        For the ``aapb`` site, return only ``AAPBExhibit`` pages; otherwise
        return only ``OpenVaultExhibit`` pages. Sorted by featured, then most
        recent ``last_published_at``.
        """
        host = getattr(self.request, 'host', None)
        if host is not None and host.name == 'aapb':
            model = AAPBExhibit
        else:
            model = OpenVaultExhibit
        return model.objects.live().order_by('-featured', '-last_published_at')
