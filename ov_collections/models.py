from typing import ClassVar

from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.api import APIField
from wagtail.blocks import RawHTMLBlock, RichTextBlock
from wagtail.fields import RichTextField, StreamField
from wagtail.images.api.fields import ImageRenditionField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtail.search import index
from wagtail_headless_preview.models import HeadlessMixin

from .blocks import AAPBRecordsBlock


class Collection(HeadlessMixin, Page):
    introduction = RichTextField(blank=True)

    content = StreamField(
        [
            ('interviews', AAPBRecordsBlock(label='Interviews', icon='openquote')),
            (
                'archival_footage',
                AAPBRecordsBlock(label='Archival Footage', icon='clipboard-list'),
            ),
            ('photographs', AAPBRecordsBlock(label='Photographs', icon='copy')),
            (
                'original_footage',
                AAPBRecordsBlock(label='Original Footage', icon='doc-full-inverse'),
            ),
            ('programs', AAPBRecordsBlock(label='Programs', icon='desktop')),
            (
                'related_content',
                AAPBRecordsBlock(label='Related Content', icon='table'),
            ),
            ('credits', RichTextBlock(icon='form')),
            (
                'heading',
                RichTextBlock(
                    form_classname='title', features=['italic'], icon='title'
                ),
            ),
            ('text', RichTextBlock()),
            ('image', ImageChooserBlock()),
            ('html', RawHTMLBlock(label='HTML')),
        ],
    )

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
        index.AutocompleteField('introduction'),
        index.SearchField('slug'),
    ]

    content_panels: ClassVar[list[FieldPanel]] = [
        *Page.content_panels,
        FieldPanel('introduction'),
        MultiFieldPanel(
            [FieldPanel('cover_image'), FieldPanel('hero_image')], heading='Images'
        ),
        FieldPanel('content'),
    ]

    api_fields: ClassVar[list[APIField]] = [
        APIField('title'),
        APIField('introduction'),
        APIField(
            'cover_image',
            serializer=ImageRenditionField('fill-1920x1080'),
        ),
        APIField(
            'hero_image',
            serializer=ImageRenditionField('fill-1600x500'),
        ),
        APIField(
            'hero_thumb',
            serializer=ImageRenditionField('fill-480x270', source='hero_image'),
        ),
        APIField('content'),
    ]
