from wagtail.snippets.models import register_snippet

from .models import Author
from .views import AuthorAdminViewSet


register_snippet(Author, viewset=AuthorAdminViewSet)
