from utils.viewsets import ResourceListViewSet, ResourceDetailViewSet
from rest_framework import viewsets, status
from rest_framework.response import Response

from ..models import Machine
from .machine_serializers import MachineListSerializer, MachineDetailSerializer

from django.shortcuts import get_object_or_404

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


class MachineUpdateViewSet(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        name = kwargs['machine_pk']
        machine = get_object_or_404(Machine.objects.all(), name=name)
        return Response(status=status.HTTP_202_ACCEPTED)
