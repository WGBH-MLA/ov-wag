from django.utils.functional import cached_property

from wagtail.admin.ui.tables import Column, UpdatedAtColumn
from wagtail.admin.viewsets.chooser import ChooserViewSet
from wagtail.admin.views.generic.chooser import ChooseView, ChooseResultsView
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetChooserViewSet

from .widgets import AdminAuthorChooser


class AuthorChooseViewMixin:
    """Mixin for author chooser views with custom template and queryset"""
    results_template_name = "authors/chooser/results.html"

    def get_object_list(self):
        return self.model_class.objects.only('name', 'title', 'image')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the chosen_url_name to the template for our custom results display
        context['chosen_url_name'] = self.chosen_url_name
        return context


class AuthorChooseView(AuthorChooseViewMixin, ChooseView):
    @property
    def columns(self):
        return super().columns + [
            Column("title", label="Title"),
        ]


class AuthorChooseResultsView(AuthorChooseViewMixin, ChooseResultsView):
    """Results view for AJAX/pagination requests"""
    pass


class AuthorChooserViewSet(SnippetChooserViewSet):
    icon = "user"

    form_fields = ['name', 'title']
    choose_one_text = "Choose an author"
    choose_another_text = "Choose another author"

    choose_view_class = AuthorChooseView
    choose_results_view_class = AuthorChooseResultsView

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
