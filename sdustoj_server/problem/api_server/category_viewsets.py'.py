from utils.viewsets import ResourceListViewSet, ResourceDetailViewSet

from ..models import Category, Node
from .category_serializers import CategorySerializer, NodeSerializer

from user.api_server.permission import IsCategoryAdmin


class CategoryListViewSet(ResourceListViewSet):
    queryset = Category
    serializer_class = CategorySerializer
    permission_classes = (IsCategoryAdmin,)


class CategoryDetailViewSet(ResourceDetailViewSet):
    queryset = Category
    serializer_class = CategorySerializer
    permission_classes = (IsCategoryAdmin,)
