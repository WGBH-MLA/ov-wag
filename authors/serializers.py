from rest_framework.fields import Field
from rest_framework.serializers import Serializer, ModelSerializer
from ov_wag.serializers import ImageSerializedField
from authors.models import Author


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']
