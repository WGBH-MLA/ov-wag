from typing import ClassVar

from django.core.files.storage import default_storage
from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.api import APIField
from wagtail.blocks import RawHTMLBlock, RichTextBlock
from wagtail.fields import RichTextField, StreamField
from wagtail.images.api.fields import ImageRenditionField
from wagtail.models import Page
from wagtail.search import index
from wagtail_headless_preview.models import HeadlessMixin

from .blocks import AAPBRecordsBlock


class BaseCollection(HeadlessMixin, Page):
    """Abstract base class for collection pages"""

    class Meta:
        abstract = True

    introduction = RichTextField(blank=True)

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

    featured = models.BooleanField(default=False)

    def get_hero_thumb_url(self):
        if self.hero_image:

            default_storage.querystring_expire = 604800
            url = self.hero_image.get_rendition('fill-480x270').url
            default_storage.querystring_expire = 3600
            return url
        return ''

    search_fields: ClassVar[list[index.SearchField]] = [
        *Page.search_fields,
        index.AutocompleteField('introduction'),
        index.FilterField('featured'),
        index.SearchField('slug'),
        index.SearchField('get_hero_thumb_url'),
    ]

    content_panels: ClassVar[list[FieldPanel]] = [
        *Page.content_panels,
        FieldPanel('introduction'),
        MultiFieldPanel(
            [FieldPanel('cover_image'), FieldPanel('hero_image')], heading='Images'
        ),
    ]

    promote_panels: ClassVar[list[FieldPanel]] = [
        FieldPanel(
            'featured',
            heading='Featured Collection',
            help_text='Featured collections will be displayed on the home page, and listed first on the collections page.',  # noqa: E501
        ),
        *Page.promote_panels,
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
    ]


class OpenVaultCollection(BaseCollection):
    """Original collection page with OV-specific content blocks."""

    class Meta:
        verbose_name = 'Open Vault Collection'
        verbose_name_plural = 'Open Vault Collections'

    parent_page_types: ClassVar[list[str]] = ['home.OpenVaultHomePage']
    subpage_types: ClassVar[list[str]] = []

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
            ('html', RawHTMLBlock(label='HTML')),
        ],
    )

    content_panels: ClassVar[list[FieldPanel]] = [
        *BaseCollection.content_panels,
        FieldPanel('content'),
    ]

    promote_panels: ClassVar[list[FieldPanel]] = BaseCollection.promote_panels

    api_fields: ClassVar[list[APIField]] = [
        *BaseCollection.api_fields,
        APIField('content'),
    ]
