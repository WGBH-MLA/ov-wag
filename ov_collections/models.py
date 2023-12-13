from typing import ClassVar

from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.api import APIField
from wagtail.blocks import (
    CharBlock,
    ListBlock,
    RichTextBlock,
    TextBlock,
    RawHTMLBlock,
)
from wagtail.fields import RichTextField, StreamField
from wagtail.images.api.fields import ImageRenditionField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtail.search import index
from wagtail_headless_preview.models import HeadlessMixin

from .blocks import ContentBlock, ContentImageBlock, AAPBRecordsBlock


class Collection(HeadlessMixin, Page):
    introduction = RichTextField(blank=True)

    content = StreamField(
        [
            (
                'interviews',
                ListBlock(
                    ContentImageBlock(label='Interview', icon='openquote'),
                    icon='openquote',
                ),
            ),
            (
                'archival_footage',
                ListBlock(ContentImageBlock(label='Footage', icon='form'), icon='form'),
            ),
            (
                'photographs',
                ListBlock(
                    ContentImageBlock(label='Photograph', icon='image'), icon='image'
                ),
            ),
            (
                'original_footage',
                ListBlock(
                    ContentImageBlock(label='Footage', icon='doc-full-inverse'),
                    icon='doc-full-inverse',
                ),
            ),
            (
                'programs',
                ListBlock(
                    ContentBlock(label='Program', icon='clipboard-list'),
                    icon='clipboard-list',
                ),
            ),
            (
                'related_content',
                ListBlock(
                    ContentBlock(label='Content', icon='list-ul'), icon='list-ul'
                ),
            ),
            ('credits', RichTextBlock()),
            ('heading', CharBlock(form_classname='title')),
            ('text', TextBlock()),
            ('image', ImageChooserBlock()),
            ('html', RawHTMLBlock()),
        ],
        use_json_field=True,
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

    aapb_records = StreamField(
        [
            ('aapb_record_group', AAPBRecordsBlock()),
        ],
        default='',
        use_json_field=True,
    )

    search_fields: ClassVar[list[index.SearchField]] = [
        *Page.search_fields,
        index.SearchField('introduction'),
    ]

    content_panels: ClassVar[list[FieldPanel]] = [
        *Page.content_panels,
        FieldPanel('introduction'),
        MultiFieldPanel(
            [FieldPanel('cover_image'), FieldPanel('hero_image')], heading='Images'
        ),
        FieldPanel('content'),
        FieldPanel('aapb_records'),
    ]

    api_fields: ClassVar[list[APIField]] = [
        APIField('title'),
        APIField('introduction'),
        APIField(
            'cover_image',
            serializer=ImageRenditionField('fill-1600x500'),
        ),
        APIField(
            'hero_image',
            serializer=ImageRenditionField('fill-1920x1080'),
        ),
        APIField(
            'hero_thumb',
            serializer=ImageRenditionField('fill-480x270', source='hero_image'),
        ),
        APIField('content'),
        APIField('aapb_records'),
    ]
