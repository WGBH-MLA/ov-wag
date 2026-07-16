from django.templatetags.static import static
from django.utils.html import format_html
from wagtail import hooks
from wagtail.snippets.models import register_snippet

from tags.views import TagsSnippetViewSet

register_snippet(TagsSnippetViewSet)

@hooks.register('insert_global_admin_css')
def global_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static('ov_collections/css/admin.css'),
    )
