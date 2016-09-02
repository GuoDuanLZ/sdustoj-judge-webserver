from rest_framework.serializers import ModelSerializer
from ..models import Client
from datetime import datetime


class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ('last_update_time', 'id', 'creator', 'create_time', 'updater', 'update_time')

    def create(self, validated_data):
        validated_data['last_update_time'] = datetime.now()
        return super().create(validated_data)
