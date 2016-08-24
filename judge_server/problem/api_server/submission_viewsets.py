from rest_framework import viewsets, response, mixins
from utils.mixins import UserCreateModelMixin
from utils.viewsets import FilterViewSet

from ..models import Submission
from .submission_serializers import SubmissionSerializer

from ..models import SubmissionMessage
from .submission_serializers import SubmissionMessageSerializer

from ..models import SubmissionCode
from .submission_serializers import SubmissionCodeInfoSerializer

from ..models import SubmissionDetail
from ..documents import CodeInfo
from .submission_serializers import SubmissionDetailSerializer

from user.api_server.permission import IsCategoryAdmin

from django.shortcuts import get_object_or_404

from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer, AdminRenderer
from .renderers import *


class SubmissionListViewSet(mixins.ListModelMixin, UserCreateModelMixin,
                            FilterViewSet):
    required_user_fields = [('user', 'username', False)]

    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    search_fields = ('user', 'client')

    permission_classes = (IsCategoryAdmin,)

    renderer_classes = (JSONRenderer, SubmissionListRenderer, BrowsableAPIRenderer, AdminRenderer)


class SubmissionDetailViewSet(mixins.RetrieveModelMixin, FilterViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    permission_classes = (IsCategoryAdmin,)

    renderer_classes = (JSONRenderer, SubmissionListRenderer, BrowsableAPIRenderer, AdminRenderer)


class SubmissionMessageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubmissionMessage.objects.all()
    serializer_class = SubmissionMessageSerializer
    lookup_field = 'submission_id'

    permission_classes = (IsCategoryAdmin,)


class SubmissionMoreDetailViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubmissionDetail.objects.all()
    serializer_class = SubmissionDetailSerializer
    lookup_field = 'submission_id'

    permission_classes = (IsCategoryAdmin,)


class SubmissionCodeInfoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubmissionCode.objects.all()
    serializer_class = SubmissionCodeInfoSerializer
    lookup_field = 'submission_id'

    permission_classes = (IsCategoryAdmin,)


class SubmissionCodeViewSet(viewsets.GenericViewSet):
    lookup_field = 'name'

    permission_classes = (IsCategoryAdmin,)

    def retrieve(self, request, *args, **kwargs):
        code_info = get_object_or_404(SubmissionCode.objects.all(), submission_id=kwargs['info_submission_id'])

        sid = str(code_info.submission_id)
        name = kwargs['name']

        code = CodeInfo.get_code(sid, name)

        return response.Response({'submission': int(sid), 'name': name, 'code': code})
