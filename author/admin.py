from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from .models import Author


class AuthorAdmin(ModelAdmin):
    """Author admin page"""

    model = Author
    menu_label = 'Authors'
    menu_icon = 'group'
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('name', 'image', 'bio')
    search_fields = ('name', 'bio')


modeladmin_register(AuthorAdmin)
