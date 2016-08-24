from rest_framework import filters
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, DestroyModelMixin, ListModelMixin
from utils.viewsets import NestedResourceListViewSet, NestedResourceDetailViewSet
from utils.viewsets import NestedResourceReadOnlyViewSet
from utils.filters import resource_ordering

from user.api_server.permission import IsProblemAdmin, IsCategoryAdmin, ProblemAdminEditable

from ..models import MetaProblem, Problem
from .problem_serializers import ProblemListSerializer, ProblemDetailSerializer, ProblemReadOnlySerializer
from .problem_filters import ProblemFilter

from ..models import Limit
from .problem_serializers import LimitListSerializer, LimitDetailSerializer
from .problem_filters import LimitFilter

from ..models import TestData, ProblemTestData
from .problem_serializers import TestDataSerializer, TestDataRelationSerializer

from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from rest_framework.renderers import AdminRenderer, JSONRenderer, BrowsableAPIRenderer
from .renderers import *


class ProblemListViewSet(NestedResourceListViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemListSerializer
    permission_classes = (IsProblemAdmin,)

    filter_class = ProblemFilter
    search_fields = ('title', 'introduction', 'id', 'content')
    ordering_fields = resource_ordering + ('id', 'title')

    parent_queryset = MetaProblem.objects.all()
    parent_lookup = 'meta_problem_pk'
    parent_pk_field = 'id'
    parent_related_name = 'meta_problem'

    renderer_classes = (JSONRenderer, ProblemInMetaListRenderer, BrowsableAPIRenderer, AdminRenderer)


class ProblemDetailViewSet(NestedResourceDetailViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemDetailSerializer
    permission_classes = (IsProblemAdmin,)

    parent_queryset = MetaProblem.objects.all()
    parent_lookup = 'meta_problem_pk'
    parent_pk_field = 'id'
    parent_related_name = 'meta_problem'

    renderer_classes = (JSONRenderer, ProblemInMetaDetailRenderer, BrowsableAPIRenderer, AdminRenderer)


class ProblemReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemReadOnlySerializer
    permission_classes = (IsCategoryAdmin,)

    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = ProblemFilter
    search_fields = ('title', 'introduction', 'id', 'content')
    ordering_fields = resource_ordering + ('id', 'title')

    renderer_classes = (JSONRenderer, ProblemListRenderer, BrowsableAPIRenderer, AdminRenderer)


class LimitListViewSet(NestedResourceListViewSet):
    queryset = Limit.objects.all()
    serializer_class = LimitListSerializer
    permission_classes = (ProblemAdminEditable,)

    filter_class = LimitFilter
    search_fields = ('title', 'introduction', 'id')
    ordering_fields = resource_ordering + ('id', 'title', 'time_limit', 'memory_limit', 'length_limit')

    parent_queryset = Problem.objects.all()
    parent_lookup = 'problem_pk'
    parent_pk_field = 'id'
    parent_related_name = 'problem'

    renderer_classes = (JSONRenderer, ProblemLimitRenderer, BrowsableAPIRenderer, AdminRenderer)


class LimitDetailViewSet(NestedResourceDetailViewSet):
    queryset = Limit.objects.all()
    serializer_class = LimitDetailSerializer
    permission_classes = (IsProblemAdmin,)

    parent_queryset = Problem.objects.all()
    parent_lookup = 'problem_pk'
    parent_pk_field = 'id'
    parent_related_name = 'problem'

    renderer_classes = (JSONRenderer, ProblemLimitRenderer, BrowsableAPIRenderer, AdminRenderer)


class TestDataReadOnlyViewSet(NestedResourceReadOnlyViewSet):
    queryset = TestData.objects.all()
    serializer_class = TestDataSerializer
    permission_classes = (IsCategoryAdmin,)

    parent_queryset = Problem.objects.all()
    parent_lookup = 'problem_pk'
    parent_pk_field = 'id'
    parent_related_name = 'problem'

    renderer_classes = (JSONRenderer, ProblemTestDataRenderer, BrowsableAPIRenderer, AdminRenderer)

    def list(self, request, *args, **kwargs):
        problem = Problem.objects.all().filter(id=kwargs['problem_pk'])
        print(TestData.objects.filter(problem=problem))
        return super().list(request, *args, **kwargs)


class TestDataRelationViewSet(RetrieveModelMixin, DestroyModelMixin, NestedResourceListViewSet):
    queryset = ProblemTestData.objects.all()
    serializer_class = TestDataRelationSerializer
    permission_classes = (IsProblemAdmin,)

    parent_queryset = Problem.objects.all()
    parent_lookup = 'problem_pk'
    parent_pk_field = 'id'
    parent_related_name = 'problem'

    renderer_classes = (JSONRenderer, ProblemTestDataRelRenderer, BrowsableAPIRenderer, AdminRenderer)


class DescriptionInProblemViewSet(ListModelMixin, GenericViewSet):
    permission_classes = (IsCategoryAdmin,)

    def list(self, request, *args, **kwargs):
        problem = get_object_or_404(Problem.objects.all(), id=kwargs['problem_pk'])
        description = problem.description
        return Response({
            'id': description.id if description is not None else None,
            'content': description.content if description is not None else None
        })


class SampleInProblemViewSet(ListModelMixin, GenericViewSet):
    permission_classes = (IsCategoryAdmin,)

    def list(self, request, *args, **kwargs):
        problem = get_object_or_404(Problem.objects.all(), id=kwargs['problem_pk'])
        sample = problem.sample
        return Response({
            'id': sample.id if sample is not None else None,
            'content': sample.content if sample is not None else None
        })
