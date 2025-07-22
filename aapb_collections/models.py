from ov_collections.models import CollectionPage
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


class AAPBCollection(CollectionPage):
    """
    AAPB Collection model.
    """

    # class Meta:
    #     verbose_name = "AAPB Collection"
    #     verbose_name_plural = "AAPB Collections"
    # ordering = ['title']

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
        *CollectionPage.content_panels,
        FieldPanel('content'),
    ]
    api_fields: ClassVar[list[APIField]] = [
        *CollectionPage.api_fields,
        APIField('content'),
    ]
