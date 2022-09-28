from rest_framework.fields import Field
from ov_wag.serializers import ImageSerializedField
from authors.serializers import AuthorSerializer


class ExhibitStubSerializer(Field):
    image = ImageSerializedField()
    authors = AuthorSerializer(many=True)

    def to_representation(self, value):
        return {
            'id': value.exhibit_id,
            'title': value.title,
            'cover_image': self.image.to_representation(value.cover_image),
            'authors': self.authors.to_representation(value.authors),
        }


class ExhibitsSerializer(Field):
    exhibit = ExhibitStubSerializer()
    image = ImageSerializedField()

    def to_representation(self, value):
        return [self.exhibit.to_representation(exhibit) for exhibit in value.all()]
