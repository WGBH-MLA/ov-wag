from django.utils.functional import cached_property

from wagtail.admin.ui.tables import Column, UpdatedAtColumn
from wagtail.admin.viewsets.chooser import ChooserViewSet
from wagtail.admin.views.generic.chooser import ChooseView
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetChooserViewSet

from .widgets import AdminAuthorChooser


class AuthorChooseView(ChooseView):
    results_template_name = "authors/chooser/results.html"

    def get_object_list(self):
        return self.model_class.objects.only('name', 'title', 'image')

    @property
    def columns(self):
        return super().columns + [  # [UpdatedAtColumn()]
            Column("title", label="Title"),
        ]


class AuthorChooserViewSet(SnippetChooserViewSet):
    icon = "user"

    form_fields = ['name', 'title']
    choose_one_text = "Choose an author"
    choose_another_text = "Choose another author"

    choose_view_class = AuthorChooseView

    @cached_property
    def widget_class(self):
        return AdminAuthorChooser(model=self.model, icon=self.icon)


class AuthorAdminViewSet(SnippetViewSet):
    """Author admin page"""

    model = 'authors.Author'
    menu_label = 'Authors'
    icon = 'group'
    list_display = ('name', 'image', 'title', UpdatedAtColumn())
    add_to_settings_menu = False
    exclude_from_explorer = False
    search_fields = ('name', 'bio', 'title')
    add_to_admin_menu = True
    chooser_viewset_class = AuthorChooserViewSet
