from rest_framework import serializers

from ..models import Client
from problem.models import Submission


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id_str', 'full_name')
        read_only_fields = ('id_str', 'full_name')


class SubmissionSerializer(serializers.ModelSerializer):
    eid = serializers.CharField(source='environment')
    code = serializers.CharField(write_only=True, style={'base_template': 'textarea.html'})

    class Meta:
        model = Submission
        fields = ('problem', 'user', 'contest', 'eid', 'code')
