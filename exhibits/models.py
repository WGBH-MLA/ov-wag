from typing import ClassVar

from django.db import models
from modelcluster.fields import ParentalKey
from pydantic import BaseModel
from rest_framework import serializers
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.api import APIField
from wagtail.blocks import RawHTMLBlock, RichTextBlock
from wagtail.fields import StreamField
from wagtail.images.api.fields import ImageRenditionField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Orderable, Page
from wagtail.search import index
from wagtail_footnotes.blocks import RichTextBlockWithFootnotes
from wagtail_headless_preview.models import HeadlessMixin

from authors.serializers import AuthorSerializer
from ov_collections.blocks import AAPBRecordsBlock
from ov_wag.serializers import FootnotesSerializer


class RichTextFootnotesBlock(RichTextBlockWithFootnotes):
    def __init__(
        self,
        features=(
            'bold',
            'italic',
            'h2',
            'h3',
            'h4',
            'ol',
            'ul',
            'hr',
            'link',
            'image',
            'blockquote',
            'footnotes',
        ),
        **kwargs,
    ):
        super().__init__(features=features, **kwargs)


class ExhibitsOrderable(Orderable):
    """Ordered list of other exhibits related to this exhibit"""

    page = ParentalKey('exhibits.ExhibitPage', related_name='other_exhibits', null=True)
    exhibit = models.ForeignKey(
        'exhibits.ExhibitPage',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    panels: ClassVar[list[FieldPanel]] = [FieldPanel('exhibit')]

    @property
    def title(self):
        return self.exhibit.title

    @property
    def cover_image(self):
        return self.exhibit.cover_image

    @property
    def authors(self):
        return self.exhibit.authors

    api_fields: ClassVar[list[APIField]] = [
        APIField('exhibit_id'),
        APIField('title'),
        APIField(
            'cover_image',
            serializer=ImageRenditionField('fill-320x100'),
        ),
        APIField('authors', serializer=AuthorSerializer(many=True)),
    ]


class OtherExhibitsField(APIField):
    """API field for other_exhibits"""

    class Meta:
        model = ExhibitsOrderable


class OtherExhibitsSerializer(serializers.ModelSerializer):
    """Serializer for other_exhibits field"""

    cover_image = ImageRenditionField('fill-320x100')

    class Meta:
        model = ExhibitsOrderable
        fields: ClassVar[list[str]] = [
            'exhibit_id',
            'title',
            'cover_image',
        ]


class ImageApiSchema(BaseModel):
    url: str
    width: int
    height: int
    alt: str


class AuthorAPISchema(BaseModel):
    """API schema for Author"""

    id: int
    name: str
    image: ImageApiSchema


class ExhibitsApiSchema(BaseModel):
    id: int
    title: str
    cover_image: ImageApiSchema
    cover_thumb: ImageApiSchema
    hero_image: ImageApiSchema
    hero_thumb: ImageApiSchema
    authors: list[AuthorAPISchema]


class ExhibitPageApiSchema(ExhibitsApiSchema):
    body: list[str]


class ExhibitPage(HeadlessMixin, Page):
    body = StreamField(
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
            ('text', RichTextFootnotesBlock()),
            ('image', ImageChooserBlock()),
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
            ('html', RawHTMLBlock(label='HTML')),
        ],
    )

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

    search_fields: ClassVar[list[index.SearchField]] = [
        *Page.search_fields,
        index.AutocompleteField('body'),
        index.FilterField('featured'),
    ]

    content_panels: ClassVar[list[FieldPanel]] = [
        *Page.content_panels,
        MultiFieldPanel(
            [FieldPanel('cover_image'), FieldPanel('hero_image')], heading='Images'
        ),
        FieldPanel('body', classname='collapsed'),
        InlinePanel('authors', heading='Author(s)'),
        InlinePanel('other_exhibits', heading='Other Exhibits', max_num=3),
        InlinePanel('footnotes', label='Footnotes'),
    ]

    promote_panels: ClassVar[list[FieldPanel]] = [
        FieldPanel(
            'featured',
            heading='Featured Exhibit',
            help_text='Featured exhibits will be displayed on the home page, and as "other exhibits" on other exhibit pages.',  # noqa: E501
        ),
        *Page.promote_panels,
    ]

    api_fields: ClassVar[list[APIField]] = [
        APIField('title'),
        APIField('body'),
        APIField(
            'cover_image',
            serializer=ImageRenditionField('fill-1920x1080'),
        ),
        APIField(
            'cover_thumb',
            serializer=ImageRenditionField('fill-480x270', source='cover_image'),
        ),
        APIField(
            'hero_image',
            serializer=ImageRenditionField('fill-1600x500'),
        ),
        APIField(
            'hero_thumb',
            serializer=ImageRenditionField('fill-480x270', source='hero_image'),
        ),
        APIField('authors'),
        APIField('footnotes', serializer=FootnotesSerializer()),
        OtherExhibitsField(
            'other_exhibits', serializer=OtherExhibitsSerializer(many=True)
        ),
    ]
