from ov_collections.blocks import AAPBRecordsBlock
from ov_collections.models import BaseCollection
from wagtail.fields import StreamField
from wagtail.images.api.fields import ImageRenditionField
from django.db import models
from wagtail.blocks import RichTextBlock
from typing import ClassVar
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.api import APIField
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase


class SortChoices(models.TextChoices):
    TITLE = 'title', 'Title'
    DATE = 'date', 'Date'
    RANDOM = 'random', 'Random'


class SortOrder(models.TextChoices):
    ASCENDING = 'asc', 'Ascending'
    DESCENDING = 'desc', 'Descending'


class AAPBCollectionTag(TaggedItemBase):
    content_object = ParentalKey(
        'aapb_collections.AAPBCollection',
        on_delete=models.CASCADE,
        related_name='tagged_items',
    )


class AAPBCollection(BaseCollection):
    """
    AAPB Collection model
    """

    class Meta:
        verbose_name = 'AAPB Collection'
        verbose_name_plural = 'AAPB Collections'

    parent_page_types: ClassVar[list[str]] = ['home.AAPBHomePage']
    subpage_types: ClassVar[list[str]] = []

    # Fields

    content = StreamField(
        [
            (
                'background',
                RichTextBlock(label='Collection Background', icon='doc-full-inverse'),
            ),
            ('funders', RichTextBlock(icon='group')),
            ('help', RichTextBlock(icon='help')),
            (
                'resources',
                RichTextBlock(label='Other Resources', icon='doc-full-inverse'),
            ),
            (
                'terms',
                RichTextBlock(label='Suggested Searches', icon='doc-full-inverse'),
            ),
            ('timeline', RichTextBlock(icon='clock')),
        ]
    )

    featured_items = StreamField(
        [
            ('records', AAPBRecordsBlock(icon='doc-full-inverse')),
        ],
        help_text='Featured items in the collection',
        blank=True,
    )

    sort_by = models.CharField(
        max_length=8,
        choices=SortChoices.choices,
        default=SortChoices.TITLE,
        help_text='Choose how to sort the collection items.',
        blank=True,
        null=True,
    )

    sort_order = models.CharField(
        max_length=4,
        choices=SortOrder.choices,
        default=SortOrder.ASCENDING,
        help_text='Choose the order of the sorted items.',
        blank=True,
        null=True,
    )

    tags = ClusterTaggableManager(through=AAPBCollectionTag, blank=True)

    # Panels

    content_panels: ClassVar[list[FieldPanel]] = [
        *BaseCollection.content_panels,
        FieldPanel('content'),
        MultiFieldPanel(
            [FieldPanel('featured_items')],
            heading='Featured Items',
            help_text='Featured items in the collection, such as records or exhibits.',
        ),
        MultiFieldPanel(
            [
                FieldPanel('sort_by'),
                FieldPanel('sort_order'),
            ],
            heading='Sorting Options',
            help_text='Choose how to sort the collection items.',
        ),
    ]

    promote_panels: ClassVar[list[FieldPanel]] = [
        FieldPanel('tags', heading='Tags'),
        *BaseCollection.promote_panels,
    ]

    # API Fields

    api_fields: ClassVar[list[APIField]] = [
        *BaseCollection.api_fields,
        APIField('content'),
        APIField('featured_items'),
        APIField('sort_by'),
        APIField('sort_order'),
        APIField('tags'),
        APIField(
            'cover_medium',
            serializer=ImageRenditionField('fill-800x800', source='cover_image'),
        ),
        APIField(
            'cover_small',
            serializer=ImageRenditionField('fill-400x400', source='cover_image'),
        ),
    ]
