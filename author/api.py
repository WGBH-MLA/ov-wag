from wagtail.api.v2.views import BaseAPIViewSet
from .models import Author


class AuthorAPIViewSet(BaseAPIViewSet):
    model = Author
    listing_default_fields = [
        'id',
        'detail_url',
        'name',
        'image',
    ]
