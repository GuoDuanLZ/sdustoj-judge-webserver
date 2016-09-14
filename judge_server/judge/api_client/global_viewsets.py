from rest_framework import viewsets

from ..models import Environment
from .global_serializers import EnvironmentSerializer

from rest_framework.renderers import JSONRenderer


class EnvironmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Environment.objects.all()
    serializer_class = EnvironmentSerializer
    renderer_classes = (JSONRenderer,)
