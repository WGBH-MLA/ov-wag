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

    A list of AAPB records to be displayed as a group. See AAPBOptionsBlock for details
    about display options.

    Attributes:
        guids: required. List of GUIDs, separated by whitespace
        show_title: optional. Show the title of records on the page
        show_thumbnail: optional. Show the thumbnail of records on the page
        title: optional. Title of the group
    """

    guids = TextBlock(
        required=True,
        help_text='AAPB record IDs, separated by whitespace',
    )

    show_title = BooleanBlock(required=False, help_text='Show title', default=True)

    show_thumbnail = BooleanBlock(
        required=False, help_text='Show thumbnail', default=True
    )

    title = RichTextBlock(
        required=False,
        max_length=1024,
        help_text='The title of this group',
        features=['italic'],
    )
