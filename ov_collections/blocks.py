from wagtail.core.blocks import StructBlock, ListBlock, CharBlock, URLBlock
from wagtail.images.blocks import ImageChooserBlock


class ContentBlock(StructBlock):
    """Generic content block
    - title
    - image
    - link

    All fields are required
    """

    title = CharBlock(
        required=True, max_length=1024, help_text='The title of this content'
    )
    image = ImageChooserBlock(required=True)
    link = URLBlock(required=True)


class InterviewsBlock(StructBlock):
    class Meta:
        icon = 'openquote'

    interviews = ListBlock(StructBlock([('interview', ContentBlock())]))


class ArchivalFootageBlock(StructBlock):
    class Meta:
        icon = 'form'

    footage = ListBlock(StructBlock([('footage', ContentBlock())]))


class PhotographsBlock(StructBlock):
    class Meta:
        icon = 'image'

    photos = ListBlock(StructBlock([('photos', ContentBlock())]))


class OriginalFootageBlock(StructBlock):
    class Meta:
        icon = 'doc-full-inverse'

    footage = ListBlock(StructBlock([('footage', ContentBlock())]))


class ProgramsBlock(StructBlock):
    class Meta:
        icon = 'clipboard-list'

    programs = ListBlock(StructBlock([('programs', ContentBlock())]))


class RelatedContentBlock(StructBlock):
    class Meta:
        icon = 'list-ul'

    content = ListBlock(StructBlock([('related_content', ContentBlock())]))


class CreditsBlock(StructBlock):
    class Meta:
        icon = 'group'

    credits = ListBlock(StructBlock([('credits', ContentBlock())]))
