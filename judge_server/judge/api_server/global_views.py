from utils.viewsets import ResourceListViewSet, ResourceDetailViewSet
from utils.filters import resource_ordering

from user.api_server.permission import IsJudgeAdmin

from ..models import Environment
from .global_serializers import EnvironmentListSerializer, EnvironmentDetailSerializer
from .global_filters import EnvironmentFilter

from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer, AdminRenderer
from .renderers import *


class EnvironmentViewSet(ResourceListViewSet):
    queryset = Environment.objects.all()
    serializer_class = EnvironmentListSerializer
    lookup_field = 'eid'
    filter_class = EnvironmentFilter
    search_fields = ('eid', 'language')
    ordering_fields = resource_ordering + ('eid', 'language')
    permission_classes = (IsJudgeAdmin,)

    renderer_classes = (JSONRenderer, EnvironmentRenderer, BrowsableAPIRenderer, AdminRenderer)


class EnvironmentDetailViewSet(ResourceDetailViewSet):
    queryset = Environment.objects.all()
    serializer_class = EnvironmentDetailSerializer
    lookup_field = 'eid'
    permission_classes = (IsJudgeAdmin,)

    renderer_classes = (JSONRenderer, EnvironmentRenderer, BrowsableAPIRenderer, AdminRenderer)
