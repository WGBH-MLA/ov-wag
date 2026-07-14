from django.templatetags.static import static
from django.utils.html import format_html
from wagtail import hooks
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from taggit.models import Tag


class TagsSnippetViewSet(SnippetViewSet):
    panels = [FieldPanel("name"), FieldPanel("slug")]
    model = Tag
    icon = "tag"
    add_to_admin_menu = True
    menu_label = "Tags"
    menu_order = 300
    list_display = ["name", "slug"]
    search_fields = ("name",)

register_snippet(TagsSnippetViewSet)

@hooks.register('insert_global_admin_css')
def global_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static('ov_collections/css/admin.css'),
    )
