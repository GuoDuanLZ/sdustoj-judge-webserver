from utils.viewsets import ResourceListViewSet, ResourceDetailViewSet

from user.api_server.permission import IsClientAdmin

from .client_serializers import ClientSerializer
from ..models import Client

from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from .renderers import ClientRenderer


class ClientListViewSet(ResourceListViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = (IsClientAdmin,)

    renderer_classes = (JSONRenderer, ClientRenderer, BrowsableAPIRenderer)


class ClientDetailViewSet(ResourceDetailViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = (IsClientAdmin,)

    renderer_classes = (JSONRenderer, ClientRenderer, BrowsableAPIRenderer)
