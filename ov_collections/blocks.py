from wagtail.core.blocks import StructBlock, ListBlock, CharBlock, URLBlock
from wagtail.images.blocks import ImageChooserBlock


class ContentBlock(StructBlock):
    """Generic content block
    - title
    - link

    All fields are required
    """

    title = CharBlock(
        required=True, max_length=1024, help_text='The title of this content'
    )
    link = URLBlock(required=True)
    
class ContentImageBlock(ContentBlock):
    """Generic content block with image
    - image
    """

    image = ImageChooserBlock(required=True)




class InterviewsBlock(StructBlock):
    class Meta:
        icon = 'openquote'

    content = ListBlock(StructBlock([('interview', ContentImageBlock())]))


class ArchivalFootageBlock(StructBlock):
    class Meta:
        icon = 'form'

    content = ListBlock(StructBlock([('footage', ContentImageBlock())]))


class PhotographsBlock(StructBlock):
    class Meta:
        icon = 'image'

    content = ListBlock(StructBlock([('photos', ContentImageBlock())]))


class OriginalFootageBlock(StructBlock):
    class Meta:
        icon = 'doc-full-inverse'

    content = ListBlock(StructBlock([('footage', ContentImageBlock())]))


class ProgramsBlock(StructBlock):
    class Meta:
        icon = 'clipboard-list'

    content = ListBlock(StructBlock([('programs', ContentBlock())]))


class RelatedContentBlock(StructBlock):
    class Meta:
        icon = 'list-ul'

    content = ListBlock(StructBlock([('related_content', ContentBlock())]))
