from rest_framework import serializers
from utils.serializers import resource_read_only

from ..models import Environment


class EnvironmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Environment
        fields = ('eid', 'language')
        read_only_fields = resource_read_only
