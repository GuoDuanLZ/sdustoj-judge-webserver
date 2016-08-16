from utils.viewsets import ResourceListViewSet, ResourceDetailViewSet
from utils.viewsets import NestedResourceListViewSet, NestedResourceDetailViewSet
from utils.filters import resource_ordering

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
from .meta_problem_serializers import TestDataListSerializer, TestDataDetailSerializer


class MetaProblemListViewSet(ResourceListViewSet):
    queryset = MetaProblem.objects.all()
    serializer_class = MetaProblemListSerializer
    permission_classes = (IsProblemAdmin,)
    filter_class = MetaProblemFilter
    search_fields = ('title', 'introduction', 'id')
    ordering_fields = resource_ordering + ('id',)


class MetaProblemDetailViewSet(ResourceDetailViewSet):
    queryset = MetaProblem.objects.all()
    serializer_class = MetaProblemDetailSerializer
    permission_classes = (IsProblemAdmin,)

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


class DescriptionDetailViewSet(NestedResourceDetailViewSet):
    queryset = Description.objects.all()
    serializer_class = DescriptionDetailSerializer
    permission_classes = (IsProblemAdmin,)


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


class SampleDetailViewSet(NestedResourceDetailViewSet):
    queryset = Sample.objects.all()
    serializer_class = SampleDetailSerializer
    permission_classes = (IsProblemAdmin,)


class TestDataListViewSet(NestedResourceListViewSet):
    queryset = TestData.objects.all()
    serializer_class = TestDataListSerializer
    permission_classes = (IsProblemAdmin,)

    parent_queryset = MetaProblem.objects.all()
    parent_lookup = 'meta_problem_pk'
    parent_pk_field = 'id'
    parent_related_name = 'meta_problem'
    child_parent_field = 'meta_problem'


class TestDataDetailViewSet(NestedResourceDetailViewSet):
    queryset = TestData.objects.all()
    serializer_class = TestDataDetailSerializer
    permission_classes = (IsProblemAdmin,)

    def perform_destroy(self, instance):
        instance.delete_mongo_data()
        super().perform_destroy(instance)
