from redis import Redis
from rest_framework import serializers

from judge_server.redis_connections import pool
from problem import documents
from utils.serializers import resource_read_only

from ..models import Problem, SpecialJudge

from ..models import Limit
from ..models import TestData, ProblemTestData

from ..models import InvalidWord


from ..tasks import send_data_insert, send_data_delete, send_code_insert, send_code_delete



class ProblemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        exclude = ('test_data',)
        read_only_fields = resource_read_only + ('meta_problem',
                                                 'number_test_data',
                                                 'number_decorator',
                                                 'number_limit',
                                                 'number_category',
                                                 'number_node')

    def create(self, validated_data):
        description = validated_data.get('description')
        sample = validated_data.get('sample')
        meta_problem = validated_data['meta_problem']
        if description is not None and description.meta_problem != meta_problem:
            raise serializers.ValidationError('Cannot choose description from other meta problem.')
        if sample is not None and sample.meta_problem != meta_problem:
            raise serializers.ValidationError('Cannot choose sample from other meta problem.')
        return super().create(validated_data)


class ProblemDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'
        read_only_fields = resource_read_only + ('meta_problem',
                                                 'number_test_data',
                                                 'number_decorator',
                                                 'number_limit',
                                                 'number_category',
                                                 'number_node')

    def update(self, instance, validated_data):
        description = validated_data.get('description')
        sample = validated_data.get('sample')
        meta_problem = instance.meta_problem
        if description is not None and description.meta_problem != meta_problem:
            raise serializers.ValidationError('Cannot choose description from other meta problem.')
        if sample is not None and sample.meta_problem != meta_problem:
            raise serializers.ValidationError('Cannot choose sample from other meta problem.')
        return super().update(instance, validated_data)


class ProblemReadOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        exclude = ('test_data',)


class LimitListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Limit
        fields = '__all__'
        read_only_fields = resource_read_only + ('problem', 'language')

    def create(self, validated_data):
        ret = super().create(validated_data)
        ret.language = ret.environment.language
        send_data_insert.delay(mid=ret.problem.meta_problem_id)
        return ret


class LimitDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Limit
        fields = '__all__'
        read_only_fields = resource_read_only + ('problem', 'language')

    def update(self, instance, validated_data):
        ret = super().update(instance, validated_data)
        ret.language = ret.environment.language
        send_data_insert.delay(mid=ret.problem.id)
        return ret


class InvalidWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvalidWord
        fields = '__all__'
        read_only_fields = resource_read_only + ('problem',)


class TestDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestData
        fields = '__all__'


class TestDataRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemTestData
        fields = '__all__'
        read_only_fields = resource_read_only + ('problem',)

    def create(self, validated_data):
        test_data = validated_data['test_data']
        problem = validated_data['problem']
        meta_problem = problem.meta_problem
        print(test_data.meta_problem, meta_problem)
        if test_data is not None and test_data.meta_problem != meta_problem:
            raise serializers.ValidationError('Cannot choose test data from other meta problem.')
        if ProblemTestData.objects.filter(problem=problem, test_data=test_data).exists():
            raise serializers.ValidationError('Relation already exists.')
        return super().create(validated_data)


class NewProblemSerializer(serializers.ModelSerializer):
    description = serializers.CharField(write_only=True, style={'base_template': 'textarea.html'})
    sample = serializers.CharField(write_only=True, style={'base_template': 'textarea.html'})
    limits = serializers.JSONField(write_only=True)

    class Meta:
        model = Problem
        exclude = ('test_data',)
        read_only_fields = resource_read_only + ('meta_problem',
                                                 'number_test_data',
                                                 'number_decorator',
                                                 'number_limit',
                                                 'number_category',
                                                 'number_node')

    def create(self, validated_data):
        description = validated_data.pop('description')
        sample = validated_data.pop('sample')
        test_type = validated_data.pop('test_type')
        title = validated_data.pop('title')
        introduction = validated_data.pop('introduction')
        source = validated_data.pop('source')
        author = validated_data.pop('author')
        status = validated_data.pop('status')
        limits = validated_data.pop('limits')

        return Problem.create_new_problem(description, sample, limits, [], test_type,
                                          title, introduction, source, author, status)


class SpecialJudgeSerializer(serializers.ModelSerializer):
    code = serializers.CharField(write_only=True, style={'base_template': 'textarea.html'})

    class Meta:
        model = SpecialJudge
        exclude = ('problem',)
        read_only_fields = resource_read_only

    def create(self, validated_data):
        code = validated_data.pop('code')

        instance = super().create(validated_data)
        documents.SpecialJudge.set_code(str(instance.problem.meta_problem_id),
                                        str(instance.problem_id),
                                        code.encode('utf-8'))

        send_code_insert.delay(str(instance.problem.meta_problem_id),
                               str(instance.problem_id),
                               str(instance.environment_id),
                               code)

        problem = instance.problem
        problem.test_type = 'SPJ'
        problem.save()

        return instance

    def update(self, instance, validated_data):
        code = validated_data.pop('code')

        instance = super().update(instance, validated_data)
        documents.SpecialJudge.set_code(str(instance.problem.meta_problem_id),
                                        str(instance.problem_id),
                                        code.encode('utf-8'))

        send_code_insert.delay(str(instance.problem.meta_problem_id),
                               str(instance.problem_id),
                               str(instance.environment_id),
                               code)
        return instance

    @staticmethod
    def delete_mongodb(instance):
        problem = instance.problem
        problem.test_type = 'normal'
        problem.save()

        # info = {
        #     'isFiles': 'false',
        #     'sid': 'SPJ',
        #     'mid': str(instance.problem.meta_problem_id),
        #     'pid': str(instance.problem_id),
        #     'eid': str(instance.environment_id),
        #     'code': '',
        # }
        # documents.SpecialJudge.remove_code(str(instance.problem_id))
        #
        # send_code_delete.delay(instance.problem.meta_problem_id, instance.problem_id, info=info)
        pass
