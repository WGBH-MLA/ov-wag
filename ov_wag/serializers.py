from pydantic import BaseModel
from rest_framework.fields import Field
from wagtail.templatetags import wagtailcore_tags


class FootnoteAPIModel(BaseModel):
    id: int
    uuid: str
    text: str


class FootnotesSerializer(Field):
    def to_representation(self, value):
        return [
            FootnoteAPIModel(**footnote).model_dump() for footnote in value.values()
        ]


class RichTextSerializer(Field):
    def to_representation(self, value):
        return wagtailcore_tags.richtext(value)
