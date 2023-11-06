from typing import ClassVar, List

from wagtail.api.v2.views import BaseAPIViewSet

from .models import Collection


class CollectionAPIViewSet(BaseAPIViewSet):
    model = Collection

    listing_default_fields: ClassVar[List[str]] = [
        *BaseAPIViewSet.listing_default_fields,
        'title',
        'introduction',
        'cover_image',
    ]
