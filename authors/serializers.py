from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from wagtail.images.api.fields import ImageRenditionField
from authors.models import Author


class AuthorSerializer(ModelSerializer):
    image = ImageRenditionField('fill-100x100')
    author_id = PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Author
        fields = [
            'author_id',
            'name',
            'image',
        ]
