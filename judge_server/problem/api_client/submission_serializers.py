from rest_framework import serializers
from ..models import Submission, SubmissionMessage, SubmissionDetail, SubmissionCode


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ('id', 'problem', 'environment', 'submit_time', 'judge_time', 'code_length',
                  'user', 'contest', 'finished', 'status')
