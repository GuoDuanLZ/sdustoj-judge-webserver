from utils.viewsets import ResourceListViewSet, ResourceDetailViewSet
from utils.viewsets import NestedResourceListViewSet, NestedResourceDetailViewSet
from utils.filters import resource_ordering

from rest_framework import viewsets
from django.http import Http404, StreamingHttpResponse

from user.api_server.permission import IsProblemAdmin

from ..models import MetaProblem
from .meta_problem_serializers import MetaProblemListSerializer, MetaProblemDetailSerializer
from .meta_problem_filters import MetaProblemFilter

from ..models import Description
from .meta_problem_serializers import DescriptionListSerializer, DescriptionDetailSerializer
from .meta_problem_filters import DescriptionFilter

from ..models import Sample
from .meta_problem_serializers import SampleListSerializer, SampleDetailSerializer
from .meta_problem_filters import SampleFilter

from ..models import TestData
from ..documents import TestData as TestDataMongodb
from .meta_problem_serializers import TestDataListSerializer, TestDataDetailSerializer
from .meta_problem_serializers import TestFileSerializer, TestInFileSerializer, TestOutFileSerializer

from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer, AdminRenderer
from .renderers import *


class MetaProblemListViewSet(ResourceListViewSet):
    queryset = MetaProblem.objects.all()
    serializer_class = MetaProblemListSerializer
    permission_classes = (IsProblemAdmin,)
    filter_class = MetaProblemFilter
    search_fields = ('title', 'introduction', 'id')
    ordering_fields = resource_ordering + ('id',)

    renderer_classes = (JSONRenderer, MetaProblemListRenderer, BrowsableAPIRenderer, AdminRenderer)


class MetaProblemDetailViewSet(ResourceDetailViewSet):
    queryset = MetaProblem.objects.all()
    serializer_class = MetaProblemDetailSerializer
    permission_classes = (IsProblemAdmin,)

    renderer_classes = (JSONRenderer, MetaProblemDetailRenderer, BrowsableAPIRenderer, AdminRenderer)

    def perform_destroy(self, instance):
        test_data = instance.test_data.all()
        for i in test_data:
            i.delete_mongo_data()
        super().perform_destroy(instance)


class DescriptionListViewSet(NestedResourceListViewSet):
    queryset = Description.objects.all()
    serializer_class = DescriptionListSerializer
    permission_classes = (IsProblemAdmin,)

    filter_class = DescriptionFilter
    search_fields = ('title', 'introduction', 'id', 'content')
    ordering_fields = resource_ordering + ('id', 'title')

    parent_queryset = MetaProblem.objects.all()
    parent_lookup = 'meta_problem_pk'
    parent_pk_field = 'id'
    parent_related_name = 'meta_problem'
    child_parent_field = 'meta_problem'

    renderer_classes = (JSONRenderer, DescriptionListRenderer, BrowsableAPIRenderer, AdminRenderer)


class DescriptionDetailViewSet(NestedResourceDetailViewSet):
    queryset = Description.objects.all()
    serializer_class = DescriptionDetailSerializer
    permission_classes = (IsProblemAdmin,)

    renderer_classes = (JSONRenderer, DescriptionDetailRenderer, BrowsableAPIRenderer, AdminRenderer)


class SampleListViewSet(NestedResourceListViewSet):
    queryset = Sample.objects.all()
    serializer_class = SampleListSerializer
    permission_classes = (IsProblemAdmin,)

    filter_class = SampleFilter
    search_fields = ('title', 'introduction', 'id', 'content')
    ordering_fields = resource_ordering + ('id', 'title')

    parent_queryset = MetaProblem.objects.all()
    parent_lookup = 'meta_problem_pk'
    parent_pk_field = 'id'
    parent_related_name = 'meta_problem'
    child_parent_field = 'meta_problem'

    renderer_classes = (JSONRenderer, SampleListRenderer, BrowsableAPIRenderer, AdminRenderer)


class SampleDetailViewSet(NestedResourceDetailViewSet):
    queryset = Sample.objects.all()
    serializer_class = SampleDetailSerializer
    permission_classes = (IsProblemAdmin,)

    renderer_classes = (JSONRenderer, SampleDetailRenderer, BrowsableAPIRenderer, AdminRenderer)


class TestDataListViewSet(NestedResourceListViewSet):
    queryset = TestData.objects.all()
    serializer_class = TestDataListSerializer
    permission_classes = (IsProblemAdmin,)

    parent_queryset = MetaProblem.objects.all()
    parent_lookup = 'meta_problem_pk'
    parent_pk_field = 'id'
    parent_related_name = 'meta_problem'
    child_parent_field = 'meta_problem'

    renderer_classes = (JSONRenderer, TestDataListRenderer, BrowsableAPIRenderer, AdminRenderer)


class TestDataDetailViewSet(NestedResourceDetailViewSet):
    queryset = TestData.objects.all()
    serializer_class = TestDataDetailSerializer
    permission_classes = (IsProblemAdmin,)

    renderer_classes = (JSONRenderer, TestDataDetailRenderer, BrowsableAPIRenderer, AdminRenderer)

    def perform_destroy(self, instance):
        TestDataDetailSerializer.delete_mongodb(instance)
        super().perform_destroy(instance)


class TestFileUploadViewSet(NestedResourceListViewSet):
    queryset = TestData.objects.all()
    serializer_class = TestFileSerializer
    permission_classes = (IsProblemAdmin,)

    parent_queryset = MetaProblem.objects.all()
    parent_lookup = 'meta_problem_pk'
    parent_pk_field = 'id'
    parent_related_name = 'meta_problem'
    child_parent_field = 'meta_problem'

    renderer_classes = (JSONRenderer, TestDataListUploadRenderer, BrowsableAPIRenderer, AdminRenderer)


class TestInFileUploadViewSet(NestedResourceDetailViewSet):
    queryset = TestData.objects.all()
    serializer_class = TestInFileSerializer
    permission_classes = (IsProblemAdmin,)

    parent_queryset = MetaProblem.objects.all()
    parent_lookup = 'meta_problem_pk'
    parent_pk_field = 'id'
    parent_related_name = 'meta_problem'
    child_parent_field = 'meta_problem'

    renderer_classes = (JSONRenderer, TestDataDetailUploadInRenderer, BrowsableAPIRenderer, AdminRenderer)


class TestOutFileUploadViewSet(NestedResourceDetailViewSet):
    queryset = TestData.objects.all()
    serializer_class = TestOutFileSerializer
    permission_classes = (IsProblemAdmin,)

    parent_queryset = MetaProblem.objects.all()
    parent_lookup = 'meta_problem_pk'
    parent_pk_field = 'id'
    parent_related_name = 'meta_problem'
    child_parent_field = 'meta_problem'

    renderer_classes = (JSONRenderer, TestDataDetailUploadOutRenderer, BrowsableAPIRenderer, AdminRenderer)


def file_iterator(file, chunk_size=512):
    while True:
        c = file.read(chunk_size)
        if c:
            yield c
        else:
            break


class TestInFileViewSet(viewsets.ViewSet):
    permission_classes = (IsProblemAdmin,)

    def list(self, request, *args, **kwargs):
        mid = str(kwargs['meta_problem_pk'])
        tid = str(kwargs['test_pk'])

        test = getattr(TestDataMongodb, 'objects').filter(mid=mid, tid=tid).first()
        if test is None:
            raise Http404()

        res = StreamingHttpResponse(file_iterator(test.fin))
        res['Content-Type'] = 'application/octet-stream'
        res['Content-Disposition'] = 'attachment;filename='+str(tid)+'.in'

        return res


class TestOutFileViewSet(viewsets.ViewSet):
    permission_classes = (IsProblemAdmin,)

    def list(self, request, *args, **kwargs):
        mid = str(kwargs['meta_problem_pk'])
        tid = str(kwargs['test_pk'])

        test = getattr(TestDataMongodb, 'objects').filter(mid=mid, tid=tid).first()
        if test is None:
            raise Http404()

        response = StreamingHttpResponse(file_iterator(test.fout))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename='+str(tid)+'.out'

        return response
