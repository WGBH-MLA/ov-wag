from django.db.models import Q
from rest_framework.filters import BaseFilterBackend


class TagFilter(BaseFilterBackend):
    """Filter pages by tag via ``?tag=<slug or name>``.

    Multiple comma-separated tags are combined with AND, e.g.
    ``?tag=news,boston`` returns pages tagged with both. Each value is matched
    against the tag ``slug`` (exact) or ``name`` (case-insensitive).
    """

    def filter_queryset(self, request, queryset, view):
        tag_param = request.GET.get("tag")
        if not tag_param:
            return queryset

        for value in tag_param.split(","):
            value = value.strip()
            if value:
                queryset = queryset.filter(
                    Q(tags__slug=value) | Q(tags__name__iexact=value)
                )
        return queryset.distinct()
