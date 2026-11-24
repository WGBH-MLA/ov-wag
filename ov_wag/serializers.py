from pydantic import BaseModel
from rest_framework.fields import Field
from uuid import UUID


class FootnoteAPIModel(BaseModel):
    id: int
    uuid: UUID
    text: str


class FootnotesSerializer(Field):
    def to_representation(self, value):
        return [
            FootnoteAPIModel(**footnote).model_dump() for footnote in value.values()
        ]


class RichTextSerializer(Field):
    def to_representation(self, value):
        # Imported lazily: wagtail>=8 loads models when this module is imported,
        # which fails if imported from a models module during app loading.
        from wagtail.templatetags import wagtailcore_tags  # noqa: PLC0415

        return wagtailcore_tags.richtext(value)
