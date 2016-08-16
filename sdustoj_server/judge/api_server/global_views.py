from utils.viewsets import ResourceListViewSet, ResourceDetailViewSet
from utils.filters import resource_ordering

from user.api_server.permission import IsJudgeAdmin

from ..models import Environment
from .global_serializers import EnvironmentListSerializer, EnvironmentDetailSerializer
from .global_filters import EnvironmentFilter


class EnvironmentViewSet(ResourceListViewSet):
    queryset = Environment.objects.all()
    serializer_class = EnvironmentListSerializer
    lookup_field = 'eid'
    filter_class = EnvironmentFilter
    search_fields = ('eid', 'language')
    ordering_fields = resource_ordering + ('eid', 'language')
    permission_classes = (IsJudgeAdmin,)


class EnvironmentDetailViewSet(ResourceDetailViewSet):
    queryset = Environment.objects.all()
    serializer_class = EnvironmentDetailSerializer
    lookup_field = 'eid'
    permission_classes = (IsJudgeAdmin,)
