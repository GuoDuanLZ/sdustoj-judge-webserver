from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {
            'username': {'validators': [RegexValidator()]},
            'password': {'write_only': True,
                         'style': {'input_type': 'password'}}
        }
