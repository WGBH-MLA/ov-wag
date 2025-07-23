from factory import SubFactory
from wagtail_factories import ImageChooserBlockFactory, PageFactory

from .models import OpenVaultCollection


class OpenVaultCollectionFactory(PageFactory):
    cover_image = SubFactory(ImageChooserBlockFactory)
    hero_image = SubFactory(ImageChooserBlockFactory)

    class Meta:
        model = OpenVaultCollection
