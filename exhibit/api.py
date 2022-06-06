from wagtail.api.v2.views import BaseAPIViewSet
from .models import ExhibitPage


class ExhibitAPIViewSet(BaseAPIViewSet):
    model = ExhibitPage

    listing_default_fields = BaseAPIViewSet.listing_default_fields + [
        'title',
        'authors',
        'hero_thumb',
    ]
