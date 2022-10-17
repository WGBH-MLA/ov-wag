from django.db import models
from wagtail import blocks
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.search import index
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.images.api.fields import ImageRenditionField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.api import APIField
from .blocks import (
    InterviewsBlock,
    ArchivalFootageBlock,
    PhotographsBlock,
    OriginalFootageBlock,
    ProgramsBlock,
    RelatedContentBlock,
)


class Collection(Page):
    about = RichTextField(blank=True)

    content = StreamField(
        [
            ('interviews', InterviewsBlock()),
            ('archival_footage', ArchivalFootageBlock()),
            ('photographs', PhotographsBlock()),
            ('original_footage', OriginalFootageBlock()),
            ('programs', ProgramsBlock()),
            ('related_content', RelatedContentBlock()),
            ('credits', blocks.RichTextBlock()),
            ('heading', blocks.CharBlock(form_classname='title')),
            ('text', blocks.TextBlock()),
            ('image', ImageChooserBlock()),
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

    search_fields = Page.search_fields + [
        index.SearchField('about'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('about'),
        FieldPanel('cover_image'),
        FieldPanel('content'),
    ]

    api_fields = [
        APIField('title'),
        APIField('about'),
        APIField(
            'cover_image',
            serializer=ImageRenditionField('fill-1600x500'),
        ),
        APIField('content')
    ]
