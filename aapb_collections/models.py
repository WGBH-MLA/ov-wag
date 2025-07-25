from ov_collections.blocks import AAPBRecordsBlock
from ov_collections.models import BaseCollection
from wagtail.fields import RichTextField, StreamField
from django.db import models
from wagtail.blocks import RawHTMLBlock, RichTextBlock
from typing import ClassVar
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.api import APIField


class SortChoices(models.TextChoices):
    TITLE = 'title', 'Title'
    DATE = 'date', 'Date'
    RANDOM = 'random', 'Random'


class SortOrder(models.TextChoices):
    ASCENDING = 'asc', 'Ascending'
    DESCENDING = 'desc', 'Descending'


class AAPBCollection(BaseCollection):
    """
    AAPB Collection model
    """

    class Meta:
        verbose_name = "AAPB Collection"
        verbose_name_plural = "AAPB Collections"

    parent_page_types: ClassVar[list[str]] = ['home.AAPBHomePage']
    subpage_types: ClassVar[list[str]] = []

    # Fields

    content = StreamField(
        [
            ('background', RichTextBlock(icon='doc-full-inverse')),
            ('funders', RichTextBlock(icon='group')),
            ('help', RichTextBlock(icon='help')),
            ('resources', RichTextBlock(icon='doc-full-inverse')),
            ('terms', RichTextBlock(icon='doc-full-inverse')),
            ('timeline', RichTextBlock(icon='clock')),
        ]
    )

    featured_items = StreamField(
        [
            ('records', AAPBRecordsBlock(icon='doc-full-inverse')),
        ],
        help_text="Featured items in the collection, such as records or exhibits.",
        blank=True,
    )

    sort_by = models.CharField(
        max_length=8,
        choices=SortChoices.choices,
        default=SortChoices.TITLE,
        help_text="Choose how to sort the collection items.",
        blank=True,
        null=True,
    )

    sort_order = models.CharField(
        max_length=4,
        choices=SortOrder.choices,
        default=SortOrder.ASCENDING,
        help_text="Choose the order of the sorted items.",
        blank=True,
        null=True,
    )

    # Panels

    content_panels: ClassVar[list[FieldPanel]] = [
        *BaseCollection.content_panels,
        FieldPanel('content'),
        MultiFieldPanel(
            [FieldPanel('featured_items')],
            heading='Featured Items',
            help_text="Featured items in the collection, such as records or exhibits.",
        ),
        MultiFieldPanel(
            [
                FieldPanel('sort_by'),
                FieldPanel('sort_order'),
            ],
            heading='Sorting Options',
            help_text="Choose how to sort the collection items.",
        ),
    ]

    promote_panels: ClassVar[list[FieldPanel]] = BaseCollection.promote_panels

    # API Fields

    api_fields: ClassVar[list[APIField]] = [
        *BaseCollection.api_fields,
        APIField('content'),
        APIField('featured_items'),
        APIField('sort_by'),
        APIField('sort_order'),
    ]
