from django.db import models
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.api.fields import ImageRenditionField
from wagtail.search import index
from wagtail.api import APIField
from pydantic import BaseModel
from modelcluster.fields import ParentalKey
from ov_wag.serializers import RichTextSerializer, ImageSerializedField


class ExhibitsOrderable(Orderable):
    page = ParentalKey('exhibit.ExhibitPage', related_name='other_exhibits', null=True)
    exhibit = models.ForeignKey(
        'exhibit.ExhibitPage',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    panels = [FieldPanel('exhibit')]

    @property
    def title(self):
        return self.exhibit.title

    @property
    def cover_image(self):
        return self.exhibit.cover_image

    @property
    def authors(self):
        return self.exhibit.authors

    api_fields = [
        APIField('title'),
        APIField('cover_image', serializer=ImageSerializedField()),
        APIField('authors'),
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

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('body', classname='full'),
        FieldPanel('cover_image', classname='full'),
        FieldPanel('hero_image', classname='full'),
        MultiFieldPanel([InlinePanel('authors', label='Author', heading='Author(s)')]),
        MultiFieldPanel(
            [
                InlinePanel(
                    'other_exhibits', label='Other Exhibits', heading='Other Exhibits'
                )
            ]
        ),
    ]

    api_fields = [
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
