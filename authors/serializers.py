from rest_framework.fields import Field
from ov_wag.serializers import ImageSerializedField


class AuthorSerializer(Field):
    image = ImageSerializedField()

    def to_representation(self, author):
        return {
            'id': author.author_id,
            'name': author.name,
            'image': self.image.to_representation(author.image),
        }


class AuthorsSerializer(Field):
    author = AuthorSerializer()

    def to_representation(self, authors):
        return [self.author.to_representation(author) for author in authors.all()]
