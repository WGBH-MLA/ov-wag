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
    AAPB Collection model.
    """

    content = StreamField(
        [
            ('background', RichTextBlock(icon='doc-full-inverse')),
            ('featured', RichTextBlock(icon='star')),
            ('funders', RichTextBlock(icon='group')),
            ('help', RichTextBlock(icon='help')),
            ('terms', RichTextBlock(icon='doc-full-inverse')),
            ('timeline', RichTextBlock(icon='clock')),
        ]
    )

    sort_by = models.CharField(
        max_length=8,
        choices=SortChoices.choices,
        default=SortChoices.TITLE,
        help_text="Choose how to sort the collection items.",
    )

    sort_order = models.CharField(
        max_length=4,
        choices=SortOrder.choices,
        default=SortOrder.ASCENDING,
        help_text="Choose the order of the sorted items.",
    )

    content_panels: ClassVar[list[FieldPanel]] = [
        *BaseCollection.content_panels,
        FieldPanel('content'),
        FieldPanel('sort_by'),
        FieldPanel('sort_order'),
    ]

    promote_panels: ClassVar[list[FieldPanel]] = BaseCollection.promote_panels

    api_fields: ClassVar[list[APIField]] = [
        *BaseCollection.api_fields,
        APIField('content'),
        APIField('sort_by'),
        APIField('sort_order'),
    ]
