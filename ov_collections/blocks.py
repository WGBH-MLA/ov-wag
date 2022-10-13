from wagtail.core.blocks import StructBlock, ListBlock, CharBlock, URLBlock
from wagtail.images.blocks import ImageChooserBlock


class ContentBlock(StructBlock):
    title = CharBlock(
        required=True, max_length=1024, help_text='The title of this content'
    )
    image = ImageChooserBlock(required=True)
    link = URLBlock(required=True)


class InterviewsBlock(StructBlock):
    class Meta:
        icon = 'openquote'

    interviews = ListBlock(StructBlock([('interview', ContentBlock())]))
