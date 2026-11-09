from factory import SubFactory
from wagtail_factories import ImageChooserBlockFactory, PageFactory

from aapb_exhibits.models import AAPBExhibit


class AAPBExhibitPageFactory(PageFactory):
    cover_image = SubFactory(ImageChooserBlockFactory)
    hero_image = SubFactory(ImageChooserBlockFactory)

    class Meta:
        model = AAPBExhibit
