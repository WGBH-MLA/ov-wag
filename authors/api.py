from typing import ClassVar

from wagtail.api.v2.views import BaseAPIViewSet

from .models import Author


class AuthorsAPIViewSet(BaseAPIViewSet):
    model = Author
    listing_default_fields: ClassVar[list[str]] = [
        'id',
        'detail_url',
        'name',
        'image',
    ]
