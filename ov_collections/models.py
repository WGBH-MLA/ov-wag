from typing import ClassVar

from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.api import APIField
from wagtail.blocks import (
    RawHTMLBlock,
    RichTextBlock,
    TextBlock,
)
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
            ('interviews', AAPBRecordsBlock(label='Interview', icon='openquote')),
            ('archival_footage', AAPBRecordsBlock(label='Footage', icon='form')),
            ('photographs', AAPBRecordsBlock(label='Photograph', icon='image')),
            (
                'original_footage',
                AAPBRecordsBlock(label='Footage', icon='doc-full-inverse'),
            ),
            ('programs', AAPBRecordsBlock(label='Program', icon='clipboard-list')),
            (
                'related_content',
                AAPBRecordsBlock(label='Content', icon='list-ul'),
            ),
            ('credits', RichTextBlock()),
            ('heading', RichTextBlock(form_classname='title', features=['italic'])),
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
    ]
