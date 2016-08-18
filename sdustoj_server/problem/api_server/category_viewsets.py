from utils.viewsets import ResourceListViewSet, ResourceDetailViewSet
from utils.viewsets import NestedResourceListViewSet, NestedResourceDetailViewSet

from ..models import Category, Node, ProblemCategoryNode
from .category_serializers import CategorySerializer, NodeSerializer, ProblemCategoryNodeSerializer

from user.api_server.permission import IsCategoryAdmin


class CategoryListViewSet(ResourceListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsCategoryAdmin,)


class CategoryDetailViewSet(ResourceDetailViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsCategoryAdmin,)


class NodeListViewSet(NestedResourceListViewSet):
    queryset = Node.objects.filter()
    serializer_class = NodeSerializer
    permission_classes = (IsCategoryAdmin,)

    parent_queryset = Category.objects.all()
    parent_lookup = 'category_pk'
    parent_pk_field = 'id'
    parent_related_name = 'category'


class NodeDetailViewSet(NestedResourceDetailViewSet):
    queryset = Node.objects.filter()
    serializer_class = NodeSerializer
    permission_classes = (IsCategoryAdmin,)


class ProblemCategoryNodeViewSet(NestedResourceListViewSet):
    queryset = ProblemCategoryNode.objects.all()
    serializer_class = ProblemCategoryNodeSerializer
    permission_classes = (IsCategoryAdmin,)

    parent_queryset = Category.objects.all()
    parent_lookup = 'category_pk'
    parent_pk_field = 'id'
    parent_related_name = 'category'