from typing import ClassVar

from wagtail.api.v2.views import PagesAPIViewSet

from .models import Collection


class CollectionAPIViewSet(PagesAPIViewSet):
    model = Collection

    listing_default_fields: ClassVar[list[str]] = [
        *PagesAPIViewSet.listing_default_fields,
        'title',
        'introduction',
        'cover_image',
    ]
