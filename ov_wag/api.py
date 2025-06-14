from django.contrib.contenttypes.models import ContentType
from rest_framework.response import Response
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.documents.api.v2.views import DocumentsAPIViewSet
from wagtail.images.api.v2.views import ImagesAPIViewSet
from wagtail_headless_preview.models import PagePreview

from authors.api import AuthorsAPIViewSet
from exhibits.api import ExhibitsAPIViewSet
from ov_collections.api import CollectionAPIViewSet
from ov_wag.health import HealthAPIViewSet

# Create the router. 'wagtailapi' is the URL namespace
api_router = WagtailAPIRouter('wagtailapi')


class PagePreviewAPIViewSet(PagesAPIViewSet):
    known_query_parameters = PagesAPIViewSet.known_query_parameters.union(
        ['content_type', 'token']
    )

    def listing_view(self, request):
        page = self.get_object()
        serializer = self.get_serializer(page)
        return Response(serializer.data)

    def detail_view(self, request, pk):
        page = self.get_object()
        serializer = self.get_serializer(page)
        return Response(serializer.data)

    def get_object(self):
        app_label, model = self.request.GET['content_type'].split('.')
        content_type = ContentType.objects.get(app_label=app_label, model=model)

        page_preview = PagePreview.objects.get(
            content_type=content_type, token=self.request.GET['token']
        )
        page = page_preview.as_page()
        if not page.pk:
            # fake primary key to stop API URL routing from complaining
            page.pk = 0

        return page


# Add the three endpoints using the 'register_endpoint' method.
# The first parameter is the name of the endpoint (eg. pages, images). This
# is used in the URL of the endpoint
# The second parameter is the endpoint class that handles the requests
api_router.register_endpoint('authors', AuthorsAPIViewSet)
api_router.register_endpoint('collections', CollectionAPIViewSet)
api_router.register_endpoint('documents', DocumentsAPIViewSet)
api_router.register_endpoint('exhibits', ExhibitsAPIViewSet)
api_router.register_endpoint('health', HealthAPIViewSet)
api_router.register_endpoint('images', ImagesAPIViewSet)
api_router.register_endpoint('page_preview', PagePreviewAPIViewSet)
api_router.register_endpoint('pages', PagesAPIViewSet)
