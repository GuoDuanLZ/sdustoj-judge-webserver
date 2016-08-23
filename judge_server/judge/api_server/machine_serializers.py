from rest_framework import serializers
from django.contrib.auth.models import User

from ..models import Machine, Environment


class MachineListSerializer(serializers.ModelSerializer):
    environment = serializers.PrimaryKeyRelatedField(many=True, queryset=Environment.objects.all(), required=False)

    class Meta:
        model = Machine
        fields = '__all__'
        read_only_fields = ('creator', 'updater')
        extra_kwargs = {
            'settings': {'write_only': True, 'style': {'base_template': 'textarea.html'}}
        }


class MachineDetailSerializer(serializers.ModelSerializer):
    environment = serializers.PrimaryKeyRelatedField(many=True, queryset=Environment.objects.all(), required=False)

    class Meta:
        model = Machine
        fields = '__all__'
        read_only_fields = ('creator', 'updater', 'name')
