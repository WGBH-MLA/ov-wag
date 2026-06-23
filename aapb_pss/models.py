from typing import ClassVar
from django.db import models
from exhibits.models import BaseExhibitPage, BaseExhibitsOrderable
from aapb_exhibits.models import AAPBExhibit
from ov_collections.blocks import AAPBRecordsBlock
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.api import APIField
from wagtail.images.api.fields import ImageRenditionField
from wagtail.blocks import RawHTMLBlock, RichTextBlock, StreamBlock
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Orderable, Page
from wagtail.search import index

class AAPBPrimarySourceSet(Page):
    """
    AAPB PSS model
    """
    class Meta:
        verbose_name = 'AAPB Primary Source Set'
        verbose_name_plural = 'AAPB Primary Source Sets'

    parent_page_types: ClassVar[list[str]] = [
        'home.AAPBHomePage',
        'aapb_pss.AAPBPrimarySourceSet',
        ]
    subpage_types: ClassVar[list[str]] = ['aapb_pss.AAPBPrimarySourceSet']

    # Fields

    created_by = models.CharField(blank=True)

    subjects = RichTextField(
        blank=True
        )

    pdf_link = models.URLField(
        blank=True,
        help_text='Direct URL to the downloadable teaching-tips PDF.'
        )

    introduction = RichTextField(
        blank=True)

    teaching_tips = RichTextField(
        blank=True,
        help_text='Background info, essential question, discussion questions, and classroom activities.'
        )

    additional_resources = RichTextField(blank=True)
    references = RichTextField(blank=True)

    sources = StreamField(
        [
            ('records', AAPBRecordsBlock(icon='doc-full-inverse')),
        ],
        help_text='Featured sources in the Source Set',
        blank=True,
    )
    content_panels: ClassVar[list[FieldPanel]] = [
    *Page.content_panels,
        MultiFieldPanel(
            [
                FieldPanel('created_by', heading='Created by'),
                FieldPanel('subjects', heading='Subjects'),
                FieldPanel('pdf_link', heading='Teaching Tips PDF'),
                FieldPanel('introduction', heading='Introduction & Context'),
            ]
            ),

        MultiFieldPanel(
            [
            FieldPanel('sources')],
        ),

        MultiFieldPanel(
            [
                FieldPanel('teaching_tips', heading='')
            ],
            ),
        MultiFieldPanel(
            [
                FieldPanel('additional_resources', heading='Additional Resources'),
                FieldPanel('references', heading='References')
            ],
            heading='Additional Content'
        ),
        MultiFieldPanel(
            [
                InlinePanel('other_exhibits', heading='Other Exhibits'),
                InlinePanel('other_collections', heading='Other Collections'),
                InlinePanel('other_pss', heading='Other Primary Source Sets'),
            ],
            heading='You May Also Like',
        ),
    ]
    api_fields: ClassVar[list[APIField]] = [
        APIField('cover_image'),
        APIField(
            'cover_medium',
            serializer=ImageRenditionField('fill-800x800', source='cover_image')
            ),
        APIField('created_by'),
        APIField('introduction'),
        APIField('teaching_tips'),
        APIField('pdf_link'),
        APIField('additional_resources'),
        APIField('references'),
        APIField('other_exhibits'),
        APIField('other_collections'),
        APIField('other_pss'),
        APIField('sources')
    ]

class AAPBPssRelatedExhibit(Orderable):
    page = ParentalKey(
        'aapb_pss.AAPBPrimarySourceSet',
        related_name='other_exhibits',
        null=True
    )
    exhibit = models.ForeignKey(
        'aapb_exhibits.AAPBExhibit',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )

class AAPBPssRelatedCollection(Orderable):
    page = ParentalKey(
        'aapb_pss.AAPBPrimarySourceSet',
        related_name='other_collections',
        null=True
    )
    collection = models.ForeignKey(
        'aapb_collections.AAPBCollection',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )

class AAPBPssRelatedPrimarySourceSet(Orderable):
    page = ParentalKey(
        'aapb_pss.AAPBPrimarySourceSet',
        related_name='other_pss',
        null=True
    )
    pss = models.ForeignKey(
        'aapb_pss.AAPBPrimarySourceSet',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )