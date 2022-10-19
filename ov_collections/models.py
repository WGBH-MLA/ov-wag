from django.db import models
from wagtail.blocks import ListBlock, RichTextBlock, TextBlock, CharBlock
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.search import index
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.api.fields import ImageRenditionField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.api import APIField
from .blocks import ContentImageBlock, ContentBlock


class Collection(Page):
    introduction = RichTextField(blank=True)

    content = StreamField(
        [
            (
                'interviews',
                ListBlock(
                    ContentImageBlock(label='Interview', icon='openquote'),
                    icon='openquote',
                ),
            ),
            (
                'archival_footage',
                ListBlock(ContentImageBlock(label='Footage', icon='form'), icon='form'),
            ),
            (
                'photographs',
                ListBlock(
                    ContentImageBlock(label='Photograph', icon='image'), icon='image'
                ),
            ),
            (
                'original_footage',
                ListBlock(
                    ContentImageBlock(label='Footage', icon='doc-full-inverse'),
                    icon='doc-full-inverse',
                ),
            ),
            (
                'programs',
                ListBlock(
                    ContentBlock(label='Program', icon='clipboard-list'),
                    icon='clipboard-list',
                ),
            ),
            (
                'related_content',
                ListBlock(
                    ContentBlock(label='Content', icon='list-ul'), icon='list-ul'
                ),
            ),
            ('credits', RichTextBlock()),
            ('heading', CharBlock(form_classname='title')),
            ('text', TextBlock()),
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
        index.SearchField('introduction'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('introduction'),
        FieldPanel('cover_image'),
        FieldPanel('content'),
    ]

    api_fields = [
        APIField('title'),
        APIField('introduction'),
        APIField(
            'cover_image',
            serializer=ImageRenditionField('fill-1600x500'),
        ),
        APIField('content'),
    ]
