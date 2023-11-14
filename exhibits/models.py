from typing import ClassVar

from django.db import models
from modelcluster.fields import ParentalKey
from pydantic import BaseModel
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.api import APIField
from wagtail.fields import RichTextField
from wagtail.images.api.fields import ImageRenditionField
from wagtail.models import Orderable, Page
from wagtail.search import index

from authors.serializers import AuthorSerializer
from ov_wag.serializers import RichTextSerializer


class ExhibitsOrderable(Orderable):
    """Other Exhibits List"""

    page = ParentalKey('exhibits.ExhibitPage', related_name='other_exhibits', null=True)
    exhibit = models.ForeignKey(
        'exhibits.ExhibitPage',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    panels: ClassVar[list[FieldPanel]] = [FieldPanel('exhibit')]

    @property
    def title(self):
        return self.exhibit.title

    @property
    def cover_image(self):
        return self.exhibit.cover_image

    @property
    def authors(self):
        return self.exhibit.authors

    api_fields: ClassVar[list[APIField]] = [
        APIField('exhibit_id'),
        APIField('title'),
        APIField(
            'cover_image',
            serializer=ImageRenditionField('fill-320x100'),
        ),
        APIField('authors', serializer=AuthorSerializer(many=True)),
    ]


class ImageApiSchema(BaseModel):
    url: str
    width: int
    height: int
    alt: str


class ExhibitPageApiSchema(BaseModel):
    id: int
    title: str
    body: str
    cover_image: ImageApiSchema
    cover_thumb: ImageApiSchema
    hero_image: ImageApiSchema
    hero_thumb: ImageApiSchema


class ExhibitPage(Page):
    body = RichTextField(blank=True)

    cover_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    search_fields: ClassVar[list[index.SearchField]] = [
        *Page.search_fields,
        index.SearchField('body'),
    ]

    content_panels: ClassVar[list[FieldPanel]] = [
        *Page.content_panels,
        MultiFieldPanel(
            [FieldPanel('cover_image'), FieldPanel('hero_image')], heading='Images'
        ),
        FieldPanel('body', classname='collapsed'),
        InlinePanel('authors', heading='Author(s)'),
        InlinePanel('other_exhibits', heading='Other Exhibits', max_num=3),
    ]

    api_fields: ClassVar[list[APIField]] = [
        APIField('title'),
        APIField('body', serializer=RichTextSerializer()),
        APIField(
            'cover_image',
            serializer=ImageRenditionField('fill-1600x500'),
        ),
        APIField(
            'cover_thumb',
            serializer=ImageRenditionField('fill-480x270', source='cover_image'),
        ),
        APIField(
            'hero_image',
            serializer=ImageRenditionField('fill-1920x1080'),
        ),
        APIField(
            'hero_thumb',
            serializer=ImageRenditionField('fill-480x270', source='hero_image'),
        ),
        APIField('authors'),
        APIField('other_exhibits'),
    ]
