from rest_framework.fields import Field
from taggit.models import Tag
from wagtail.api import APIField
from wagtail.api.v2.views import BaseAPIViewSet

from .views import page_count


class PageCountField(Field):
    """Serializes the number of pages using a tag, across all page types."""

    def get_attribute(self, instance):
        return instance

    def to_representation(self, tag):
        return page_count(tag)


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

    # Optional: Enable basic search by name
    search_fields = ["name"]
