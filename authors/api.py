from wagtail.api.v2.views import BaseAPIViewSet
from .models import Author


class AuthorsAPIViewSet(BaseAPIViewSet):
    model = Author
