from wagtail.api.v2.views import BaseAPIViewSet
from .models import Collection


class CollectionAPIViewSet(BaseAPIViewSet):
    model = Collection

    listing_default_fields = BaseAPIViewSet.listing_default_fields + [
        'title',
        'about',
        'cover_image',
    ]
