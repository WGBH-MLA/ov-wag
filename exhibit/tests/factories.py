import factory
import wagtail_factories
from exhibit.models import ExhibitPage


class ExhibitPageFactory(wagtail_factories.PageFactory):

    cover_image = factory.SubFactory(wagtail_factories.ImageChooserBlockFactory)
    hero_image = factory.SubFactory(wagtail_factories.ImageChooserBlockFactory)

    class Meta:
        model = ExhibitPage
