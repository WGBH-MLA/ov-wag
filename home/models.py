from typing import ClassVar

from wagtail.admin.panels import FieldPanel
from wagtail.api import APIField
from wagtail.fields import RichTextField
from wagtail.models import Page


class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels: ClassVar[list[FieldPanel]] = [
        *Page.content_panels,
        FieldPanel('body', classname='full'),
    ]

    api_fields: ClassVar[list[APIField]] = [APIField('body')]
