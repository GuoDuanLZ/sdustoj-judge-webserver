from rest_framework import viewsets, mixins

from client.models import Client
from ..models import Submission, SubmissionCode, SubmissionDetail, SubmissionMessage


class SubmissionSerializer(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Client.objects.all()
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.getobject()



    def update(self, request, *args, **kwargs):
        pass