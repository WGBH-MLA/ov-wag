from rest_framework.fields import Field
from wagtail.core.templatetags import wagtailcore_tags


class ImageSerializedField(Field):
    def to_representation(self, value):
        if value:
            return {
                'url': value.file.url,
                'title': value.title,
                'width': value.width,
                'height': value.height,
            }


class RichTextSerializer(Field):
    def to_representation(self, value):
        return wagtailcore_tags.richtext(value)
