from typing import ClassVar

from wagtail.admin.panels import FieldPanel
from wagtail.api import APIField
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail_headless_preview.models import HeadlessMixin


class BaseHomePage(HeadlessMixin, Page):
    """Abstract base class for home pages in Wagtail"""

    class Meta:
        abstract = True

    body = RichTextField(blank=True)

    content_panels: ClassVar[list[FieldPanel]] = [
        *Page.content_panels,
        FieldPanel('body', classname='full'),
    ]

    api_fields: ClassVar[list[APIField]] = [APIField('body')]

    parent_page_type: ClassVar[list[str]] = ['wagtailcore.Page']


class OpenVaultHomePage(BaseHomePage):
    """
    Open Vault Home Page model
    This is the main entry point for the Open Vault site.
    """

    class Meta:
        verbose_name = 'Open Vault Home Page'
        verbose_name_plural = 'Open Vault Home Pages'

    subpage_types: ClassVar[list[str]] = [
        'ov_collections.OpenVaultCollection',
        'exhibits.ExhibitPage',
    ]


class AAPBHomePage(BaseHomePage):
    """
    AAPB Home Page model
    This is the main entry point for the AAPB site.
    """

    class Meta:
        verbose_name = 'AAPB Home Page'
        verbose_name_plural = 'AAPB Home Pages'

    subpage_types: ClassVar[list[str]] = [
        'aapb_collections.AAPBCollection',
        # 'exhibits.ExhibitPage',
    ]
