from typing import ClassVar

from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.api import APIField
from wagtail.fields import RichTextField
from wagtail.images.api.fields import ImageRenditionField
from wagtail.models import Orderable

from .widgets import AdminAuthorChooser


class BaseAuthorsOrderable(Orderable):

    class Meta:
        abstract = True

    author = models.ForeignKey(
        'authors.Author',
        on_delete=models.CASCADE,
    )

    panels: ClassVar[list[FieldPanel]] = [
        FieldPanel('author', widget=AdminAuthorChooser),
    ]

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


class AuthorsOrderable(BaseAuthorsOrderable):

    class Meta:
        unique_together = ('page', 'author')

    page = ParentalKey('exhibits.OpenVaultExhibit', related_name='authors')


class AAPBAuthorsOrderable(BaseAuthorsOrderable):

    class Meta:
        unique_together = ('page', 'author')

    page = ParentalKey('aapb_exhibits.AAPBExhibit', related_name='authors')


class Author(models.Model):
    """Author of a page"""

    name = models.CharField(max_length=100, help_text='Author name')

    title = models.CharField(max_length=200, blank=True, help_text='Author title')

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    bio = RichTextField(blank=True, help_text='Brief author bio')

    panels: ClassVar[list[FieldPanel]] = [
        MultiFieldPanel(
            [
                FieldPanel('name'),
                FieldPanel('image'),
                FieldPanel('title'),
                FieldPanel('bio'),
            ]
        )
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
