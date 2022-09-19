from rest_framework.fields import Field


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
