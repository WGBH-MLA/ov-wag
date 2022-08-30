from django.db import models
from wagtail.api import APIField
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, RichTextFieldPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey
from ov_wag.serializers import ImageSerializedField


class AuthorsOrderable(Orderable):
    page = ParentalKey('exhibit.ExhibitPage', related_name='authors', null=True)
    author = models.ForeignKey(
        'authors.Author',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    panels = [SnippetChooserPanel('author')]

    @property
    def name(self):
        return self.author.name

    @property
    def image(self):
        return self.author.image

    api_fields = [
        APIField('name'),
        APIField('image', serializer=ImageSerializedField()),
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

    panels = [
        MultiFieldPanel(
            [FieldPanel('name'), ImageChooserPanel('image'), RichTextFieldPanel('bio')]
        )
    ]

    api_fields = [
        APIField('name'),
        APIField('image'),
        APIField('bio'),
    ]

    def __str__(self):
        """str representation of this Author"""
        return self.name


register_snippet(Author)
