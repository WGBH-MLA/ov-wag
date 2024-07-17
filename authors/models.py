from typing import ClassVar

from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.admin.ui.tables import UpdatedAtColumn
from wagtail.api import APIField
from wagtail.fields import RichTextField
from wagtail.images.api.fields import ImageRenditionField
from wagtail.models import Orderable
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet


class AuthorsOrderable(Orderable):
    page = ParentalKey('exhibits.ExhibitPage', related_name='authors', null=True)
    author = models.ForeignKey(
        'authors.Author',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    panels: ClassVar[list[FieldPanel]] = [FieldPanel('author')]

    @property
    def name(self):
        return self.author.name if self.author else None

    @property
    def image(self):
        return self.author.image if self.author else None

    @property
    def bio(self):
        return self.author.bio if self.author else None

    api_fields: ClassVar[list[APIField]] = [
        APIField('author_id'),
        APIField('name'),
        APIField('image', serializer=ImageRenditionField('fill-100x100')),
        APIField('bio'),
    ]


class Author(models.Model):
    """Author of a page"""

    name = models.CharField(max_length=100, help_text='Author name')

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    bio = RichTextField(blank=True, help_text='Brief author bio')

    panels: ClassVar[list[FieldPanel]] = [
        MultiFieldPanel([FieldPanel('name'), FieldPanel('image'), FieldPanel('bio')])
    ]

    api_fields: ClassVar[list[APIField]] = [
        APIField('id'),
        APIField('name'),
        APIField('image'),
        APIField('bio'),
    ]

    def __str__(self):
        """str representation of this Author"""
        return self.name


class AuthorAdmin(SnippetViewSet):
    """Author admin page"""

    model = Author
    menu_label = 'Authors'
    icon = 'group'
    list_display = ('name', 'image', 'bio', UpdatedAtColumn())
    add_to_settings_menu = False
    exclude_from_explorer = False
    search_fields = ('name', 'bio')
    add_to_admin_menu = True


register_snippet(Author, viewset=AuthorAdmin)
