from typing import ClassVar

from wagtail.api.v2.views import PagesAPIViewSet

from aapb_exhibits.models import AAPBExhibit
from home.models import AAPBHomePage, OpenVaultHomePage
from tags.filters import TagFilter

from .models import BaseExhibitPage, OpenVaultExhibit


class ExhibitsAPIViewSet(PagesAPIViewSet):
    model = BaseExhibitPage

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
        'last_published_at',
        'cover_image',
        'cover_thumb',
        'hero_image',
        'authors',
        'featured',
        'tags',
        'special_collections',
    ]

    def get_queryset(self):
        """Return live exhibits for the current site.

        For the ``aapb`` site, return only ``AAPBExhibit`` pages; otherwise
        return only ``OpenVaultExhibit`` pages. Sorted by featured, then most
        recent ``last_published_at``.

        By default only top-level exhibits (direct children of the home page)
        are returned, so nested child exhibits are excluded. An explicit
        ``?child_of=`` or ``?descendant_of=`` query overrides this default.
        """
        host = getattr(self.request, 'host', None)
        if host is not None and host.name == 'aapb':
            model = AAPBExhibit
            home = AAPBHomePage.objects.first()
        else:
            model = OpenVaultExhibit
            home = OpenVaultHomePage.objects.first()

        qs = model.objects.live()

        if home is not None and not (
            'child_of' in self.request.GET or 'descendant_of' in self.request.GET
        ):
            qs = qs.child_of(home)

        return qs.order_by('-featured', '-last_published_at')
