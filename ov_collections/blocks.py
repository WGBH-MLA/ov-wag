from django.utils.dateparse import parse_duration
from django.utils.functional import cached_property
from wagtail.blocks import (
    BooleanBlock,
    FieldBlock,
    RichTextBlock,
    StructBlock,
    TextBlock,
    URLBlock,
)
from wagtail.images.blocks import ImageChooserBlock


class DurationBlock(FieldBlock):
    def __init__(
        self, required=True, help_text=None, format=None, validators=(), **kwargs
    ):
        self.field_options = {
            "required": required,
            "help_text": help_text,
            "validators": validators,
        }
        self.format = format
        super().__init__(**kwargs)

    @cached_property
    def field(self):
        from django.forms import DurationField

        field_kwargs = {}
        # TODO: Add an AdminDurationInput widget
        field_kwargs.update(self.field_options)
        return DurationField(**field_kwargs)

    def to_python(self, value):
        from datetime import timedelta

        if value is None or isinstance(value, timedelta):
            return value
        else:
            return parse_duration(value)

    class Meta:
        icon = "time"


class ContentBlock(StructBlock):
    """Generic External link block
    )
    from wagtail.images.blocks import ImageChooserBlock
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
        image: ImageChooserBlock. Required.
    """

    image = ImageChooserBlock(required=True)

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
    """

    guids = TextBlock(
        required=True,
        help_text='AAPB record IDs, separated by whitespace',
    )

    special_collections = TextBlock(required=False, help_text='Special collections IDs')

    show_title = BooleanBlock(
        required=False, help_text='Show asset title(s)', default=True
    )

    show_thumbnail = BooleanBlock(
        required=False, help_text='Show asset thumbnail(s)', default=True
    )

    title = RichTextBlock(
        required=False,
        max_length=1024,
        help_text='The title of this group',
        features=['italic'],
    )

    start_time = DurationBlock(
        required=False,
        help_text='Start time for the group',
    )

    end_time = DurationBlock(
        required=False,
        help_text='End time for the group',
    )

    def clean(self, value):
        data = super(AAPBRecordsBlock, self).clean(value)

        # Ensure that start_time is before end_time
        if (
            data.get('start_time')
            and data.get('end_time')
            and data['start_time'] > data['end_time']
        ):
            from django.core.exceptions import ValidationError

            raise ValidationError('Start time must be before end time')
        return data
