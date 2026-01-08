from datetime import timedelta
from django.core.exceptions import ValidationError
from django.forms import DurationField
from django.utils.dateparse import parse_duration
from django.utils.functional import cached_property
from wagtail.blocks import (
    BooleanBlock,
    FieldBlock,
    RichTextBlock,
    StructBlock,
    TextBlock,
    URLBlock,
    ChoiceBlock,
)
from wagtail.images.blocks import ImageBlock


class DurationBlock(FieldBlock):
    def __init__(
        self, required=True, help_text=None, format=None, validators=(), **kwargs
    ):
        self.field_options = {
            'required': required,
            'help_text': help_text,
            'validators': validators,
        }
        self.format = format
        super().__init__(**kwargs)

    @cached_property
    def field(self):

        field_kwargs = {}
        # TODO: Add an AdminDurationInput widget
        field_kwargs.update(self.field_options)
        return DurationField(**field_kwargs)

    def to_python(self, value):

        if value is None or isinstance(value, timedelta):
            return value
        return parse_duration(value)

    class Meta:
        icon = 'time'


class ContentBlock(StructBlock):
    """Generic External link block

    Attributes:
        title: RichTextBlock with italics only
        link: URLBlock
    """

    title = RichTextBlock(
        required=True,
        max_length=1024,
        help_text='The title of this content',
        features=['italic'],
    )
    link = URLBlock(required=True)


class ContentImageBlock(ContentBlock):
    """Generic external link block with image

    Attributes:
        image: ImageBlock. Required.
    """

    image = ImageBlock(required=True)

    def get_api_representation(self, value, context=None):
        results = super().get_api_representation(value, context)
        results['image'] = value.get('image').get_rendition('width-400').attrs_dict
        return results


class AAPBRecordsBlock(StructBlock):
    """AAPB Records block

    A list of 1 or more AAPB records to be displayed as a group.

    Attributes:
        guids: required. List of GUIDs, separated by whitespace
        show_title: Show the title of records on the page
        show_thumbnail: Show the thumbnail of records on the page
        title: Optional title of the group
        start_time: Optional start time for the group
        end_time: Optional end time for the group
        access_level: Required: access level for the group. Default: online
    """

    class Meta:
        icon = 'doc-full'
        label_format = '{title} - {guids}'
        form_template = 'ov_collections/block_forms/aapb_records_block.html'

    title = RichTextBlock(
        required=False,
        max_length=1024,
        help_text='The title of this group',
        features=['italic'],
    )

    guids = TextBlock(
        required=True,
        help_text='AAPB record IDs, separated by whitespace',
        form_classname='w-field--scrollable-textarea',
    )

    special_collections = TextBlock(required=False, help_text='Special collections IDs')

    show_title = BooleanBlock(
        required=False, help_text='Show asset title(s) for this block', default=True
    )

    show_thumbnail = BooleanBlock(
        required=False, help_text='Show asset thumbnail(s) for this block', default=True
    )

    show_sidebar = BooleanBlock(
        required=False, help_text='Include title in sidebar', default=True
    )

    start_time = DurationBlock(
        required=False,
        help_text='Start time for the group',
    )

    end_time = DurationBlock(
        required=False,
        help_text='End time for the group',
    )

    access_level = ChoiceBlock(
        required=True,
        help_text='Access level for AAPB search links in this block',
        choices=[
            ('all', 'All'),
            ('digitized', 'Digitized'),
            ('online', 'Online'),
        ],
        default='online',
    )

    def clean(self, value):
        data = super().clean(value)

        # Ensure that start_time is before end_time
        if (
            data.get('start_time')
            and data.get('end_time')
            and data['start_time'] > data['end_time']
        ):

            raise ValidationError('Start time must be before end time')
        return data

    def get_api_representation(self, value, context=None):
        results = super().get_api_representation(value, context)
        results['guids'] = value.get('guids').split()
        return results


AAPB_BLOCK_TYPES = [
    'interviews',
    'archival_footage',
    'photographs',
    'original_footage',
    'programs',
    'related_content',
]
