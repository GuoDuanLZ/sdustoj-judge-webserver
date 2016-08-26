from rest_framework import serializers
from utils.serializers import resource_read_only

from ..models import Category, Node, ProblemCategoryNode


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('problem',)
        read_only_fields = resource_read_only + ('number_node',
                                                 'number_problem')


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        exclude = ('problem',)
        read_only_fields = resource_read_only + ('number_node',
                                                 'number_problem',
                                                 'category')

    def create(self, validated_data):
        node = validated_data['parent']
        category = validated_data['category']
        if node is not None and node.category != category:
            raise serializers.ValidationError('Cannot choose node from other category.')
        return super().create(validated_data)

    def update(self, instance, validated_data):
        node = validated_data.get('parent')
        category = validated_data.get('category')
        if node is not None and node.category != category:
            raise serializers.ValidationError('Cannot choose node from other category.')
        return super().update(instance, validated_data)


class ProblemCategoryNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemCategoryNode
        fields = '__all__'
        read_only_fields = resource_read_only + ('node',
                                                 'category')


