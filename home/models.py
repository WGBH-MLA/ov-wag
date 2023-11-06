from typing import ClassVar, List

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.api import APIField
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page


class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels: ClassVar[List[FieldPanel]] = [
        *Page.content_panels,
        FieldPanel('body', classname='full'),
    ]

    api_fields: ClassVar[List[APIField]] = [APIField('body')]
