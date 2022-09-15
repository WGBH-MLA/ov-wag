from rest_framework.fields import Field
from ov_wag.serializers import ImageSerializedField


class ExhibitStubSerializer(Field):
    image_serializer = ImageSerializedField()

    def to_representation(self, value):
        return {
            'id': value.id,
            'title': value.title,
            'cover_image': self.image_serializer.to_representation(value.cover_image)
            if value.cover_image
            else None,
        }


class ExhibitsSerializer(Field):
    exhibit_serializer = ExhibitStubSerializer()
    image_serializer = ImageSerializedField()

    def to_representation(self, value):
        return [
            self.exhibit_serializer.to_representation(exhibit)
            for exhibit in value.all()
        ]
