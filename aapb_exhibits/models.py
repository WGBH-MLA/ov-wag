from exhibits.models import BaseExhibitPage, BaseExhibitsOrderable
from wagtail.fields import StreamField, RichTextField
from wagtail.blocks import RawHTMLBlock, RichTextBlock
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from ov_collections.blocks import AAPBRecordsBlock
from typing import ClassVar
from wagtail.search import index
from wagtail.api import APIField
from wagtail.models import Page
from modelcluster.fields import ParentalKey
from django.db import models


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
        ]
    )
    content_panels: ClassVar[list[FieldPanel]] = [
        *Page.content_panels,
        MultiFieldPanel(
            [
                FieldPanel('display_title'),
                InlinePanel('authors', heading='Author(s)'),
                FieldPanel('introduction', heading='Introduction'),
            ],
            heading='Intro',
        ),
        MultiFieldPanel(
            [FieldPanel('cover_image'), FieldPanel('hero_image')], heading='Images'
        ),
        FieldPanel('body', classname='collapsed'),
        MultiFieldPanel(
            [InlinePanel('child_order')],
            heading='Exhibit Pages Order',
            classname='collapsed',
        ),
        MultiFieldPanel(
            [
                InlinePanel('other_exhibits', heading='Other Exhibits', max_num=3),
                InlinePanel('footnotes', label='Footnotes'),
            ],
            heading='Additional Content',
        ),
    ]

    search_fields: ClassVar[list[index.SearchField]] = [
        *BaseExhibitPage.search_fields,
        index.AutocompleteField('body'),
    ]

    # API
    api_fields: ClassVar[list[APIField]] = [
        *BaseExhibitPage.api_fields,
        APIField('body'),
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
