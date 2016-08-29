from rest_framework import serializers
from django.contrib.auth.models import User

from django.core.validators import RegexValidator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'is_active', 'groups',
                  'date_joined', 'last_login')
        read_only_fields = ('date_joined', 'last_login')
        extra_kwargs = {
            'username': {'validators': [RegexValidator()]},
            'password': {'write_only': True,
                         'style': {'input_type': 'password'}}
        }

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.set_password(instance.password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        return instance
