from rest_framework import viewsets, mixins
from rest_framework import status
from rest_framework.response import Response

from ..models import Submission
from .submission_serializers import SubmitSerializer
from .submission_serializers import SubmissionListSerializer

from ..models import SubmissionTestInfo, SubmissionCode

from django.shortcuts import get_object_or_404


class SubmissionListViewSet(mixins.ListModelMixin, mixins.CreateModelMixin , viewsets.GenericViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionListSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = SubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED, headers=headers)


class SubmissionDetailViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionListSerializer


class SubmissionTestViewSet(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        sid = kwargs['submission_pk']
        test_info = get_object_or_404(SubmissionTestInfo.objects.all(), submission_id=sid)
        return Response(test_info.test_info, status=status.HTTP_200_OK)


class SubmissionFilesViewSet(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        sid = kwargs['submission_pk']
        code = get_object_or_404(SubmissionCode.objects.all(), submission_id=sid)
        return Response(code.file, status=status.HTTP_200_OK)


class SubmissionCodeViewSet(viewsets.ViewSet):
    def retrieve(self, request, *args, **kwargs):
        print(kwargs)
        sid = kwargs['submission_pk']
        name = kwargs['pk']
        code = get_object_or_404(SubmissionCode.objects.all(), submission_id=sid)
        content = code.get_code(name)
        print(content)
        return Response(content, status=status.HTTP_200_OK)
