from rest_framework import serializers
from utils.serializers import resource_read_only

from ..models import MetaProblem, Description, Sample, TestData


class MetaProblemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaProblem
        fields = '__all__'
        read_only_fields = resource_read_only + ('number_description',
                                                 'number_sample',
                                                 'number_test_data',
                                                 'number_virtual_judge',
                                                 'number_problem')


class MetaProblemDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaProblem
        fields = '__all__'
        read_only_fields = resource_read_only + ('number_description',
                                                 'number_sample',
                                                 'number_test_data',
                                                 'number_virtual_judge',
                                                 'number_problem')

    # def delete(self):


class DescriptionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = '__all__'
        read_only_fields = resource_read_only + ('number_problem', 'meta_problem')
        extra_kwargs = {
            'content': {'write_only': True}
        }


class DescriptionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = '__all__'
        read_only_fields = resource_read_only + ('number_problem', 'meta_problem')


class SampleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample
        fields = '__all__'
        read_only_fields = resource_read_only + ('number_problem', 'meta_problem')
        extra_kwargs = {
            'content': {'write_only': True}
        }


class SampleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample
        fields = '__all__'
        read_only_fields = resource_read_only + ('number_problem', 'meta_problem')


class TestDataMixin(object):
    def get_test_data(self, validated_data):
        test_in = validated_data.pop('get_test_in')
        test_out = validated_data.pop('get_test_out')

        test_in = test_in if test_in is not None else ''
        test_out = test_out if test_out is not None else ''

        validated_data['in_size'] = len(test_in) if test_in is not None else 0
        validated_data['out_size'] = len(test_out) if test_out is not None else 0

        return test_in, test_out

    def set_test_data(self, instance, test_in, test_out):
        instance.set_test_in(test_in)
        instance.set_test_out(test_out)


class TestDataListSerializer(serializers.ModelSerializer, TestDataMixin):
    test_in = serializers.CharField(write_only=True, allow_null=True, source='get_test_in',
                                    style={'base_template': 'textarea.html'})
    test_out = serializers.CharField(write_only=True, allow_null=True, source='get_test_out',
                                     style={'base_template': 'textarea.html'})

    class Meta:
        model = TestData
        fields = '__all__'
        read_only_fields = resource_read_only + ('number_problem', 'meta_problem', 'in_size', 'out_size')

    def create(self, validated_data):
        test_in, test_out = self.get_test_data(validated_data)
        instance = super().create(validated_data)
        self.set_test_data(instance, test_in, test_out)
        return instance


class TestDataDetailSerializer(serializers.ModelSerializer, TestDataMixin):
    test_in = serializers.CharField(allow_null=True, source='get_test_in', style={'base_template': 'textarea.html'})
    test_out = serializers.CharField(allow_null=True, source='get_test_out', style={'base_template': 'textarea.html'})

    class Meta:
        model = TestData
        fields = '__all__'
        read_only_fields = resource_read_only + ('number_problem', 'meta_problem', 'in_size', 'out_size',)

    def update(self, instance, validated_data):
        test_in, test_out = self.get_test_data(validated_data)

        instance = super().update(instance, validated_data)

        self.set_test_data(instance, test_in, test_out)
        return instance


class TestDataInUploadSerializer(serializers.ModelSerializer, TestDataMixin):
    test_in = serializers.FileField()

    class Meta:
        model = TestData
        fields = '__all__'
        read_only_fields = resource_read_only + ('title', 'introduction', 'status',
                                                 'number_problem', 'meta_problem', 'in_size', 'out_size',)
