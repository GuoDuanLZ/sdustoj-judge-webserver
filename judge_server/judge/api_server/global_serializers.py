from rest_framework import serializers
from utils.serializers import resource_read_only

from ..models import Environment

from problem.models import Limit


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

    def update(self, instance, validated_data):
        ret = super().update(instance, validated_data)
        Limit.objects.filter(environment=instance).update(language=instance.language)