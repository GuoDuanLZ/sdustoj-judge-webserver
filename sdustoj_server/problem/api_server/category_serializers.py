from rest_framework import serializers
from utils.serializers import resource_read_only

from ..models import Category, Node


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('problem',)
        read_only_fields = resource_read_only


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        exclude = ('problem',)
        read_only_fields = resource_read_only + ('number_node',
                                                 'number_problem',
                                                 'category')
