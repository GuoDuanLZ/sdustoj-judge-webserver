from utils.viewsets import ResourceListViewSet, ResourceDetailViewSet
from rest_framework import viewsets, status
from rest_framework.response import Response

from ..models import Machine
from .machine_serializers import MachineListSerializer, MachineDetailSerializer

from django.shortcuts import get_object_or_404

from user.api_server.permission import IsJudgeAdmin

from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from .renderers import *

from ..tasks import update_machine_data


class MachineListViewSet(ResourceListViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineListSerializer

    permission_classes = (IsJudgeAdmin,)

    renderer_classes = (JSONRenderer, MachineRenderer, BrowsableAPIRenderer, AdminRenderer)


class MachineDetailViewSet(ResourceDetailViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineDetailSerializer

    permission_classes = (IsJudgeAdmin,)

    lookup_field = 'name'

    renderer_classes = (JSONRenderer, MachineRenderer, BrowsableAPIRenderer, AdminRenderer)


class MachineUpdateViewSet(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        name = kwargs['machine_pk']
        machine = get_object_or_404(Machine.objects.all(), name=name)

        update_machine_data.delay(machine.name)

        return Response(status=status.HTTP_202_ACCEPTED)
