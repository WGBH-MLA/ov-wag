from typing import ClassVar

from wagtail.api.v2.filters import FieldsFilter
from wagtail.api.v2.views import PagesAPIViewSet
from .models import Collection


class TagsFilter(FieldsFilter):
    """
    Adds ?tags=foo&tags=bar support for models with a taggit-based
    `tags` manager. Handles the `tags` param itself, then strips it
    before handing off to the default FieldsFilter so it doesn't try
    (and fail) to filter on it as a plain field.
    """

    def filter_queryset(self, request, queryset, view):
        tags = request.GET.getlist('tags')
        if tags:
            queryset = queryset.filter(tags__name__in=tags).distinct()
            request.GET = request.GET.copy()
            request.GET.pop('tags', None)

        return super().filter_queryset(request, queryset, view)


class CollectionAPIViewSet(PagesAPIViewSet):
    model = Collection

    known_query_parameters: ClassVar[set] = PagesAPIViewSet.known_query_parameters.union(
        ['tags']
    )

    filter_backends: ClassVar[list] = [
        TagsFilter,
        *[b for b in PagesAPIViewSet.filter_backends if b is not FieldsFilter],
    ]

    meta_fields: ClassVar[list[str]] = [
        *PagesAPIViewSet.meta_fields,
        'last_published_at',
        'featured',
    ]
    listing_default_fields: ClassVar[list[str]] = [
        *PagesAPIViewSet.listing_default_fields,
        'title',
        'introduction',
        'cover_image',
        'hero_image',
        'last_published_at',
        'featured',
    ]

    def get_queryset(self):
        """Sort by featured, then most recent last_published_at"""
        return self.model.objects.live().order_by('-featured', '-last_published_at')
