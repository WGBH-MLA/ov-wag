from django.templatetags.static import static
from django.urls import reverse
from django.utils.html import format_html
from wagtail import hooks
from wagtail.admin.panels import FieldPanel, Panel
from wagtail.admin.ui.tables import Column
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from taggit.models import Tag

from .models import OVCollectionTag


def _tag_through_models():
    """All TaggedItemBase through-models that link pages to tags."""
    from aapb_collections.models import AAPBCollectionTag
    from aapb_exhibits.models import AAPBExhibitTag
    from exhibits.models import OpenVaultExhibitTag

    return (
        OVCollectionTag,
        OpenVaultExhibitTag,
        AAPBExhibitTag,
        AAPBCollectionTag,
    )


def tagged_pages(tag):
    """Return every page that uses the given tag, across all page types."""
    pages = []
    if not (tag and tag.pk):
        return pages
    for through_model in _tag_through_models():
        tagged_items = through_model.objects.filter(tag=tag).select_related(
            "content_object"
        )
        for item in tagged_items:
            page = item.content_object
            if page is not None:
                pages.append(page)
    return pages


def page_count(tag):
    """Number of pages using the tag, across all page types."""
    return sum(
        through_model.objects.filter(tag=tag).count()
        for through_model in _tag_through_models()
    )


class PageCountColumn(Column):
    """List column showing how many pages use a tag, across all page types."""

    def get_value(self, instance):
        return page_count(instance)


class RelatedPagesPanel(Panel):
    """Read-only panel listing the pages that use the current tag."""

    class BoundPanel(Panel.BoundPanel):
        template_name = "ov_collections/panels/related_pages.html"

        def get_context_data(self, parent_context=None):
            context = super().get_context_data(parent_context)
            tag = self.instance
            related_pages = []
            for page in tagged_pages(tag):
                page.edit_url = reverse(
                    "wagtailadmin_pages:edit", args=[page.pk]
                )
                related_pages.append(page)
            context["related_pages"] = related_pages
            return context


class TagsSnippetViewSet(SnippetViewSet):
    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
        RelatedPagesPanel(heading="Pages with this tag"),
    ]
    model = Tag
    icon = "tag"
    add_to_admin_menu = True
    menu_label = "Tags"
    menu_order = 400
    list_display = ["name", "slug", PageCountColumn("page_count", label="Pages")]
    search_fields = ("name",)

register_snippet(TagsSnippetViewSet)

@hooks.register('insert_global_admin_css')
def global_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static('ov_collections/css/admin.css'),
    )
