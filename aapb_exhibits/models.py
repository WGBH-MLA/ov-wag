from exhibits.models import BaseExhibitPage, BaseExhibitsOrderable
from wagtail.fields import StreamField, RichTextField
from wagtail.blocks import RawHTMLBlock, RichTextBlock
from wagtail.images.api.fields import ImageRenditionField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from ov_collections.blocks import AAPBRecordsBlock, VimeoVideoBlock, YouTubeVideoBlock
from typing import ClassVar
from wagtail.search import index
from wagtail.api import APIField
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from django.db import models


class AAPBExhibitTag(TaggedItemBase):
    content_object = ParentalKey(
        'aapb_exhibits.AAPBExhibit',
        on_delete=models.CASCADE,
        related_name='tagged_items',
    )


class AAPBExhibit(BaseExhibitPage):
    """AAPB Exhibit Page model"""

    class Meta:
        verbose_name = 'AAPB Exhibit'
        verbose_name_plural = 'AAPB Exhibits'

    parent_page_types: ClassVar[list[str]] = [
        'home.AAPBHomePage',
        'aapb_exhibits.AAPBExhibit',
    ]
    subpage_types: ClassVar[list[str]] = ['aapb_exhibits.AAPBExhibit']

    # Fields

    introduction = RichTextField(blank=True)

    body = StreamField(
        [
            (
                'heading',
                RichTextBlock(
                    form_classname='title', features=['italic'], icon='title'
                ),
            ),
            (
                'subheading',
                RichTextBlock(
                    form_classname='title', features=['italic'], icon='title'
                ),
            ),
            ('text', RichTextBlock()),
            ('html', RawHTMLBlock()),
            ('records', AAPBRecordsBlock()),
            ('vimeo', VimeoVideoBlock(label='Vimeo')),
            ('youtube', YouTubeVideoBlock(label='YouTube')),
        ]
    )

    tags = ClusterTaggableManager(through=AAPBExhibitTag, blank=True)

    content_panels: ClassVar[list[FieldPanel]] = [
        *BaseExhibitPage.content_panels,
        MultiFieldPanel(
            [
                InlinePanel('authors', heading='Author(s)'),
                FieldPanel('introduction', heading='Introduction'),
            ],
            heading='Introduction',
        ),
        FieldPanel('body', classname='collapsed'),
        MultiFieldPanel(
            [
                InlinePanel('other_exhibits', heading='Other Exhibits', max_num=3),
                InlinePanel('footnotes', label='Footnotes'),
                InlinePanel(
                    'child_order',
                    label='Child Exhibit page order',
                    classname='collapsed',
                ),
            ],
            heading='Additional Content',
        ),
    ]

    promote_panels: ClassVar[list[FieldPanel]] = [
        FieldPanel('tags', heading='Tags'),
        *BaseExhibitPage.promote_panels,
    ]

    search_fields: ClassVar[list[index.SearchField]] = [
        *BaseExhibitPage.search_fields,
        index.AutocompleteField('body'),
        index.SearchField('tags', partial_match=True),
    ]

    # API
    api_fields: ClassVar[list[APIField]] = [
        *BaseExhibitPage.api_fields,
        APIField('introduction'),
        APIField('body'),
        APIField('tags'),
        APIField('cover_image'),
        APIField(
            'cover_medium',
            serializer=ImageRenditionField('fill-800x800', source='cover_image'),
        ),
        APIField(
            'cover_small',
            serializer=ImageRenditionField('fill-400x400', source='cover_image'),
        ),
    ]


class AAPBOtherExhibits(BaseExhibitsOrderable):

    exhibit = models.ForeignKey(
        'aapb_exhibits.AAPBExhibit',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )

    page = ParentalKey(
        'aapb_exhibits.AAPBExhibit', related_name='other_exhibits', null=True
    )


class AAPBExhibitsChildOrder(BaseExhibitsOrderable):
    """Orderable model to relate AAPBExhibit pages
    as children of other AAPBExhibit pages"""

    class Meta:
        verbose_name = 'AAPB Exhibit page'
        verbose_name_plural = 'AAPB Exhibit pages'

    exhibit = models.ForeignKey(
        'aapb_exhibits.AAPBExhibit',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    page = ParentalKey(
        'aapb_exhibits.AAPBExhibit', related_name='child_order', null=True
    )
