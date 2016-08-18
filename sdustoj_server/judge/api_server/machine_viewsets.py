from utils.viewsets import ResourceListViewSet, ResourceDetailViewSet

from ..models import Machine
from .machine_serializers import MachineListSerializer, MachineDetailSerializer

from user.api_server.permission import IsJudgeAdmin


class MachineListViewSet(ResourceListViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineListSerializer

    permission_classes = (IsJudgeAdmin,)


class MachineDetailViewSet(ResourceDetailViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineDetailSerializer

    permission_classes = (IsJudgeAdmin,)

    lookup_field = 'name'
