from rest_framework import viewsets, mixins

from judge.models import Machine
from .submission_serializer import StatusSerializer, ResultSerializer


class StatusViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Machine.objects.all()
    serializer_class = StatusSerializer
    lookup_field = 'name'

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class ResultViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Machine.objects.all()
    serializer_class = ResultSerializer
    lookup_field = 'name'

    def update(self, request, *args, **kwargs):

        if request.data.get('msg') == '':
            request.data['msg'] = None
        if request.data.get('tid') == '':
            request.data['tid'] = None

        return super().update(request, *args, **kwargs)
