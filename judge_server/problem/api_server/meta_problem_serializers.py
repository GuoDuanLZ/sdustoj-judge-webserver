from rest_framework import serializers
from utils.serializers import resource_read_only

from .. import models, documents

from ..tasks import send_data_insert, send_data_delete


class MetaProblemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MetaProblem
        fields = '__all__'
        read_only_fields = resource_read_only + ('number_description',
                                                 'number_sample',
                                                 'number_test_data',
                                                 'number_virtual_judge',
                                                 'number_problem')


class MetaProblemDetailSerializer(MetaProblemListSerializer):
    pass


class DescriptionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Description
        fields = '__all__'
        read_only_fields = resource_read_only + ('number_problem', 'meta_problem')
        extra_kwargs = {
            'content': {'write_only': True}
        }


class DescriptionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Description
        fields = '__all__'
        read_only_fields = resource_read_only + ('number_problem', 'meta_problem')


class SampleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sample
        fields = '__all__'
        read_only_fields = resource_read_only + ('number_problem', 'meta_problem')
        extra_kwargs = {
            'content': {'write_only': True}
        }


class SampleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sample
        fields = '__all__'
        read_only_fields = resource_read_only + ('number_problem', 'meta_problem')


class TestDataListSerializer(serializers.ModelSerializer):
    test_in = serializers.CharField(write_only=True, allow_null=True,
                                    style={'base_template': 'textarea.html'})
    test_out = serializers.CharField(write_only=True, allow_null=True,
                                     style={'base_template': 'textarea.html'})

    class Meta:
        model = models.TestData
        fields = '__all__'
        read_only_fields = resource_read_only + ('number_problem', 'meta_problem', 'in_size', 'out_size')

    def create(self, validated_data):
        test_in = validated_data.pop('test_in')
        if test_in is not None:
            test_in = test_in.encode('utf-8')
        test_out = validated_data.pop('test_out')
        if test_out is not None:
            test_out = test_out.encode('utf-8')
        instance = super().create(validated_data)
        documents.TestData.set_data(str(instance.meta_problem_id),
                                    str(instance.id),
                                    test_in,
                                    test_out)
        send_data_insert.delay(instance.meta_problem_id, instance.id)
        return instance


class TestDataDetailSerializer(serializers.ModelSerializer):
    test_in = serializers.CharField(allow_null=True, source='get_test_in', style={'base_template': 'textarea.html'})
    test_out = serializers.CharField(allow_null=True, source='get_test_out', style={'base_template': 'textarea.html'})

    class Meta:
        model = models.TestData
        fields = '__all__'
        read_only_fields = resource_read_only + ('number_problem', 'meta_problem', 'in_size', 'out_size',)

    def update(self, instance, validated_data):
        test_in = validated_data.pop('test_in')
        if test_in is not None:
            test_in = test_in.encode('utf-8')
        test_out = validated_data.pop('test_out')
        if test_out is not None:
            test_out = test_out.encode('utf-8')
        instance = super().update(instance, validated_data)
        documents.TestData.set_data(str(instance.meta_problem_id),
                                    str(instance.id),
                                    test_in,
                                    test_out)
        send_data_insert.delay(instance.meta_problem_id, instance.id)
        return instance

    @staticmethod
    def delete_mongodb(instance):
        documents.TestData.remove_data(str(instance.meta_problem_id),
                                       str(instance.id))
        send_data_delete.delay(instance.meta_problem_id, instance.id)


class TestFileSerializer(serializers.ModelSerializer):
    test_in = serializers.FileField(allow_null=True, allow_empty_file=True, write_only=True)
    test_out = serializers.FileField(allow_null=True, allow_empty_file=True, write_only=True)

    class Meta:
        model = models.TestData
        fields = '__all__'
        read_only_fields = resource_read_only + ('number_problem', 'meta_problem', 'in_size', 'out_size')

    def create(self, validated_data):
        test_in = validated_data.pop('test_in')
        test_out = validated_data.pop('test_out')
        instance = super().create(validated_data)

        documents.TestData.write_data(str(instance.meta_problem_id),
                                      str(instance.id),
                                      test_in,
                                      test_out)
        send_data_insert.delay(instance.meta_problem_id, instance.id)
        return instance


class TestInFileSerializer(serializers.ModelSerializer):
    test_in = serializers.FileField(allow_null=True, allow_empty_file=True, write_only=True)

    class Meta:
        model = models.TestData
        fields = '__all__'
        read_only_fields = resource_read_only + ('number_problem', 'meta_problem', 'in_size', 'out_size')

    def update(self, instance, validated_data):
        test_in = validated_data.pop('test_in')
        instance = super().update(instance, validated_data)

        documents.TestData.write_data(str(instance.meta_problem_id),
                                      str(instance.id),
                                      test_in=test_in,
                                      test_out=False)
        send_data_insert.delay(instance.meta_problem_id, instance.id)
        return instance


class TestOutFileSerializer(serializers.ModelSerializer):
    test_out = serializers.FileField(allow_null=True, allow_empty_file=True, write_only=True)

    class Meta:
        model = models.TestData
        fields = '__all__'
        read_only_fields = resource_read_only + ('number_problem', 'meta_problem', 'in_size', 'out_size')

    def update(self, instance, validated_data):
        test_out = validated_data.pop('test_out')
        instance = super().update(instance, validated_data)

        documents.TestData.write_data(str(instance.meta_problem_id),
                                      str(instance.id),
                                      test_in=False,
                                      test_out=test_out)
        send_data_insert.delay(instance.meta_problem_id, instance.id)
        return instance
