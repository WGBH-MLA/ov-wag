from wagtail.blocks import (
    BooleanBlock,
    RichTextBlock,
    StructBlock,
    TextBlock,
    URLBlock,
)
from wagtail.images.blocks import ImageChooserBlock


class ContentBlock(StructBlock):
    """Generic content block

    This is the base block for all content blocks. All fields are required

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
    """Generic content block with image

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

    A list of AAPB records to be displayed as a group. The records can be displayed in
    different ways, depending on the options selected.

    Attributes:
        ids: required. List of GUIDs, separated by whitespace
        show_title: optional
        show_thumbnail: optional
        show_description: optional
    """

    ids = TextBlock(
        required=True,
        help_text='AAPB record IDs, separated by whitespace',
    )

    show_title = BooleanBlock(required=False, help_text='Show title', default=True)

    show_thumbnail = BooleanBlock(
        required=False, help_text='Show thumbnail', default=True
    )

    show_description = BooleanBlock(
        required=False, help_text='Show description', default=False
    )
