from rest_framework import serializers
from utils.serializers import resource_read_only

from ..models import Environment


class EnvironmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Environment
        fields = '__all__'
        read_only_fields = resource_read_only


class EnvironmentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Environment
        fields = '__all__'
        read_only_fields = resource_read_only + ('eid',)
