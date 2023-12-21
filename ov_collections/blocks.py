from wagtail.blocks import (
    BooleanBlock,
    RichTextBlock,
    StructBlock,
    TextBlock,
    URLBlock,
)
from wagtail.images.blocks import ImageChooserBlock


class ContentBlock(StructBlock):
    """Generic External link block

    This is the base block for a generic external link. All fields are required

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
    """

    guids = TextBlock(
        required=True,
        help_text='AAPB record IDs, separated by whitespace',
    )

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
