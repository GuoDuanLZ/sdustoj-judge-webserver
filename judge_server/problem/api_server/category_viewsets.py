from utils.viewsets import ResourceListViewSet, ResourceDetailViewSet
from utils.viewsets import NestedResourceListViewSet, NestedResourceDetailViewSet

from ..models import Category, Node, ProblemCategoryNode
from .category_serializers import CategorySerializer, NodeSerializer, ProblemCategoryNodeSerializer

from user.api_server.permission import IsCategoryAdmin

from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer, AdminRenderer
from .renderers import *


class CategoryListViewSet(ResourceListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsCategoryAdmin,)

    renderer_classes = (JSONRenderer, CategoryRenderer, BrowsableAPIRenderer, AdminRenderer)


class CategoryDetailViewSet(ResourceDetailViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsCategoryAdmin,)

    renderer_classes = (JSONRenderer, CategoryRenderer, BrowsableAPIRenderer, AdminRenderer)


class NodeListViewSet(NestedResourceListViewSet):
    queryset = Node.objects.filter()
    serializer_class = NodeSerializer
    permission_classes = (IsCategoryAdmin,)

    filter_fields = ('parent',)

    parent_queryset = Category.objects.all()
    parent_lookup = 'category_pk'
    parent_pk_field = 'id'
    parent_related_name = 'category'

    renderer_classes = (JSONRenderer, CategoryNodeRenderer, BrowsableAPIRenderer, AdminRenderer)


class NodeDetailViewSet(NestedResourceDetailViewSet):
    queryset = Node.objects.filter()
    serializer_class = NodeSerializer
    permission_classes = (IsCategoryAdmin,)

    renderer_classes = (JSONRenderer, CategoryNodeRenderer, BrowsableAPIRenderer, AdminRenderer)


class ProblemCategoryNodeViewSet(NestedResourceListViewSet):
    queryset = ProblemCategoryNode.objects.all()
    serializer_class = ProblemCategoryNodeSerializer
    permission_classes = (IsCategoryAdmin,)

    parent_queryset = Node.objects.all()
    parent_lookup = 'node_pk'
    parent_pk_field = 'id'
    parent_related_name = 'node'

    def create(self, request, *args, **kwargs):
        node = self.get_parent(kwargs)
        category = node.category
        extra_data = self.extra_data
        extra_data['category'] = category

        return super().create(request, *args, **kwargs)

    renderer_classes = (JSONRenderer, CategoryNodeProblemRelationRenderer, BrowsableAPIRenderer, AdminRenderer)


class ProblemCategoryNodeDetailViewSet(NestedResourceDetailViewSet):
    queryset = ProblemCategoryNode.objects.all()
    serializer_class = ProblemCategoryNodeSerializer
    permission_classes = (IsCategoryAdmin,)

    parent_queryset = Node.objects.all()
    parent_lookup = 'node_pk'
    parent_pk_field = 'id'
    parent_related_name = 'node'

    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, AdminRenderer)