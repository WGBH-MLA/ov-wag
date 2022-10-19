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
    content = ListBlock(ContentBlock())

    def get_api_representation(self, values, context=None):
        return list(values.get('content'))


class ContentListImageBlock(StructBlock):
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


class ArchivalFootageBlock(ContentListImageBlock):
    class Meta:
        icon = 'form'


class PhotographsBlock(ContentListImageBlock):
    class Meta:
        icon = 'image'


class OriginalFootageBlock(ContentListImageBlock):
    class Meta:
        icon = 'doc-full-inverse'


class ProgramsBlock(ContentListBlock):
    class Meta:
        icon = 'clipboard-list'


class RelatedContentBlock(ContentListBlock):
    class Meta:
        icon = 'list-ul'
