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

    def get_api_representation(self, value, context=None):
        results = super().get_api_representation(value, context)
        results['image'] = value.get('image').get_rendition('width-400').attrs_dict
        return results
        # return {
        #     'title': value.get('title'),
        #     'link': value.get('link'),
        #     'image': value.get('image').get_rendition('width-1000').attrs_dict,
        # }


class ContentListBlock(StructBlock):
    """Content List Block
    A ListBlock of ContentBlocks
    """
    content = ListBlock(ContentBlock())

    def get_api_representation(self, values, context=None):
        return list(values.get('content'))


class ContentListImageBlock(StructBlock):
    """Content List Block
    A ListBlock of ContentImageBlocks
    """
    content = ListBlock(ContentImageBlock())

    def get_api_representation(self, values, context=None):
        if values:
            serializer = ContentImageBlock()
            contents = values.get('content')
            return [
                serializer.get_api_representation(interview, context)
                for interview in contents
            ]


class InterviewsBlock(ContentListImageBlock):
    class Meta:
        icon = 'openquote'

class ArchivalFootageBlock(StructBlock):
    class Meta:
        icon = 'form'

    content = ListBlock(ContentImageBlock())


class PhotographsBlock(StructBlock):
    class Meta:
        icon = 'image'

    content = ListBlock(ContentImageBlock())


class OriginalFootageBlock(StructBlock):
    class Meta:
        icon = 'doc-full-inverse'

    content = ListBlock(ContentImageBlock())


class ProgramsBlock(StructBlock):
    class Meta:
        icon = 'clipboard-list'

    content = ListBlock(ContentBlock())


class RelatedContentBlock(StructBlock):
    class Meta:
        icon = 'list-ul'

    def get_api_representation(self, values, context=None):
        return list(values.get('content'))

    content = ListBlock(ContentBlock())
