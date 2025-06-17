from wagtail.api.v2.views import PagesAPIViewSet
from rest_framework.response import Response


class HealthAPIViewSet(PagesAPIViewSet):
    def listing_view(self, request):
        return Response({'status': 'ok'})
