from django.db import models
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.search import index
from wagtail.api import APIField
from pydantic import BaseModel


class ImageMetaApiSchema(BaseModel):
    download_url: str


class ImageApiSchema(BaseModel):
    id: int
    title: str
    meta: ImageMetaApiSchema


class ExhibitPageApiSchema(BaseModel):
    id: int
    title: str
    body: str
    cover_image: ImageApiSchema


class ExhibitPage(Page):
    body = RichTextField(blank=True)

    cover_image = models.ForeignKey(
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
        FieldPanel('body', classname="full"),
        MultiFieldPanel([InlinePanel('authors', label='Author', heading='Author(s)')]),
    ]

    api_fields = [
        APIField('body'),
        APIField('cover_image'),
    ]
