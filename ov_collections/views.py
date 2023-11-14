from typing import ClassVar

from wagtail.api.v2.views import BaseAPIViewSet

from .models import Collection


class CollectionAPIViewSet(BaseAPIViewSet):
    model = Collection

    listing_default_fields: ClassVar[list[str]] = [
        *BaseAPIViewSet.listing_default_fields,
        'title',
        'introduction',
        'cover_image',
    ]
