from django.db.models import Q
from rest_framework.fields import Field
from rest_framework.filters import BaseFilterBackend
from taggit.models import Tag
from wagtail.api import APIField
from wagtail.api.v2.filters import OrderingFilter
from wagtail.api.v2.views import BaseAPIViewSet

from .views import page_count


class PageCountField(Field):
    """Serializes the number of pages using a tag, across all page types."""

    def get_attribute(self, instance):
        return instance

    def to_representation(self, tag):
        return page_count(tag)


class TagSearchFilter(BaseFilterBackend):
    """Case-insensitive ?search= across the viewset's ``search_fields``.

    ``Tag`` is not registered with the Wagtail search backend, so this does a
    simple database lookup instead of Wagtail's index-based ``SearchFilter``.
    """

    def filter_queryset(self, request, queryset, view):
        search_query = request.GET.get("search")
        search_fields = getattr(view, "search_fields", None)
        if not search_query or not search_fields:
            return queryset

        lookup = Q()
        for field in search_fields:
            lookup |= Q(**{f"{field}__icontains": search_query})
        return queryset.filter(lookup)



class TagsAPIViewSet(BaseAPIViewSet):
    model = Tag
    # Fields to expose on the API
    body_fields = BaseAPIViewSet.body_fields + [
        "name",
        "slug",
        APIField("page_count", serializer=PageCountField(read_only=True)),
    ]
    listing_default_fields = BaseAPIViewSet.listing_default_fields + [
        "name",
        "slug",
        "page_count",
    ]
    name = "tags"

    # Enable ?order=name, ?order=-slug, ?order=random, and ?search=<query>
    filter_backends = [OrderingFilter, TagSearchFilter]

    # Fields searched by ?search= (case-insensitive, database lookup)
    search_fields = ["name", "slug"]
