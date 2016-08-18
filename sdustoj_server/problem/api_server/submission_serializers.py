from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.db import models

from ..models import Submission, SubmissionTest, SubmissionCode
from ..models import ProblemTestData


class SubmissionSerializer(serializers.ModelSerializer):
    code=serializers.CharField(style={'base_template': 'textarea.html'})
    class Meta:
        model = Submission
        fields =('id','environment','problem','code',)

    def create(self, validated_data):

        test_info={}
        problem=validated_data.get('problem')
        test_data=problem.test_data.all()
        for test in test_data:
            test_info[str(test.id)] = None
        submission_test = SubmissionTest(test_info=test_info)
        submission_test.save()
        validated_data['test_info'] = submission_test
        code=validated_data.pop('code')
        instance = super().create(validated_data)
        submission_code = SubmissionCode(submission=instance,code=code)
        submission_code.save()
        return  instance

class SubmissionCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionCode
        fields = '__all__'


class SubmissionTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionTest
        fields = '__all__'
