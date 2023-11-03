from wagtail.admin.edit_handlers import FieldPanel
from wagtail.api import APIField
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page


class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = [*Page.content_panels, FieldPanel('body', classname='full')]

    api_fields = [APIField('body')]
