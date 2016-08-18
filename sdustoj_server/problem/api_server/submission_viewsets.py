from rest_framework import mixins, viewsets
from rest_framework.response import Response

from django.shortcuts import get_object_or_404


from .submission_serializers import SubmissionSerializer, SubmissionCodeSerializer, SubmissionTestSerializer

from ..models import Submission, SubmissionCode, SubmissionTest





class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    lookup_field = 'id'


class SubmissionCodeViewSet(viewsets.ModelViewSet):
    queryset = SubmissionCode.objects.all()
    serializer_class = SubmissionCodeSerializer
    lookup_field = 'id'

    # def list(self, request, *args, **kwargs):
    #     submission = get_object_or_404(Submission.objects, id=kwargs['submission_pk'])
    #     self.queryset = submission.code.all()
    #     return super().list(request, *args, **kwargs)


class SubmissionTestViewSet(viewsets.ModelViewSet):
    queryset = SubmissionTest.objects.all()
    serializer_class = SubmissionTestSerializer
    lookup_field = 'id'

    # def list(self, request, *args, **kwargs):
    #     submission = get_object_or_404(Submission.objects, id=kwargs['submission_pk'])
    #     instance = submission.test_info
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)
