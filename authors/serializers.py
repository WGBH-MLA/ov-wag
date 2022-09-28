from rest_framework.serializers import ModelSerializer
from wagtail.images.api.fields import ImageRenditionField
from authors.models import Author


class AuthorSerializer(ModelSerializer):
    image = ImageRenditionField('fill-100x100')

    class Meta:
        model = Author
        fields = ['name', 'image']
