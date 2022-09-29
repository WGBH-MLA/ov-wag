from factory import SubFactory
from wagtail_factories import ImageChooserBlockFactory, PageFactory
from exhibit.models import ExhibitPage


class ExhibitPageFactory(PageFactory):

    cover_image = SubFactory(ImageChooserBlockFactory)
    hero_image = SubFactory(ImageChooserBlockFactory)
    # other_exhibits =

    class Meta:
        model = ExhibitPage
