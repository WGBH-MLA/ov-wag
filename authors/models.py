from django.db import models
from wagtail.api import APIField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable
from wagtail.images.api.fields import ImageRenditionField
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey


class AuthorsOrderable(Orderable):
    page = ParentalKey('exhibit.ExhibitPage', related_name='authors', null=True)
    author = models.ForeignKey(
        'authors.Author',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    panels = [FieldPanel('author')]

    @property
    def name(self):
        return self.author.name

    @property
    def image(self):
        return self.author.image

    api_fields = [
        APIField('name'),
        APIField('image', serializer=ImageRenditionField('fill-100x100')),
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
        MultiFieldPanel([FieldPanel('name'), FieldPanel('image'), FieldPanel('bio')])
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
