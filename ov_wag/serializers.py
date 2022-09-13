from rest_framework.fields import Field
from wagtail.core.templatetags import wagtailcore_tags


class ImageSerializedField(Field):
    def to_representation(self, value):
        return {
            'url': value.file.url,
            'title': value.title,
            'width': value.width,
            'height': value.height,
        }


class RichTextSerializer(Field):
    def to_representation(self, value):
        return wagtailcore_tags.richtext(value)


class AuthorsSerializer(Field):
    def get_attribute(self, instance):
        return instance

    def to_representation(self, value):
        authors = value.exhibit.authors
        image_serializer = ImageSerializedField()
        return [
            {
                'id': author.id,
                'name': author.name,
                'image': image_serializer.to_representation(author.image),
            }
            for author in authors.all()
        ]
