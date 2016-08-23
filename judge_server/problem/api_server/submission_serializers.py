from rest_framework import serializers
from ..models import Submission, SubmissionCode, SubmissionDetail, SubmissionMessage
from ..documents import CodeInfo

from judge_server.redis_connections import pool
from redis import Redis

from rest_framework.serializers import ValidationError
from judge_server.conf_parser import MAX_OLEN
from json import dumps

from judge.models import Machine

from rest_framework import filters
from .submission_filters import SubmissionFilter


class SubmissionSerializer(serializers.ModelSerializer):
    problem_title = serializers.CharField(read_only=True, source='problem.title')
    language = serializers.CharField(read_only=True, source='environment')
    code = serializers.CharField(write_only=True, style={'base_template': 'textarea.html'})

    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = SubmissionFilter

    search_fields = ('problem__title',)

    class Meta:
        model = Submission
        fields = '__all__'
        read_only_fields = ('submit_time', 'judge_time', 'code_length',
                            'client', 'user', 'contest', 'finished', 'status')
        extra_kwargs = {
            'environment': {'write_only': True}
        }

    def create(self, validated_data):
        environment = validated_data['environment']
        problem = validated_data['problem']
        limit = problem.limit.filter(environment=environment).first()
        if limit is None:
            raise ValidationError('Environments selected not supported.')

        code = validated_data.pop('code')
        validated_data['code_length'] = len(code)

        instance = super().create(validated_data)

        instance.code = SubmissionCode()
        instance.code.info = ['code']
        instance.code.save()

        instance.message = SubmissionMessage()
        instance.message.save()

        instance.detail = SubmissionDetail()
        instance.detail.info = {}
        test_data = instance.problem.test_data.all().values('id')
        for i in test_data:
            instance.detail.info[str(i['id'])] = '--'
        instance.detail.save()

        CodeInfo.set_code(str(instance.id), 'code', code.encode('utf-8'))

        r = Redis(connection_pool=pool)
        info = dumps({
            'isFiles': 'false',
            'sid': str(instance.id),
            'mid': str(instance.problem.meta_problem_id),
            'pid': str(instance.problem_id),
            'eid': str(instance.environment_id),
            'tid': [str(i['id']) for i in test_data],
            'tl': str(limit.time_limit),
            'ml': str(limit.memory_limit),
            'cl': str(limit.length_limit),
            'ol': str(MAX_OLEN),
            'ttype': problem.test_type,
            'code': code
        })
        print(info)
        r.rpush(self._get_queue_name(instance), info)

        return instance

    @staticmethod
    def _get_queue_name(instance):
        machines_ok = set()
        for i in instance.environment.machine.values('id'):
            machines_ok.add(i['id'])

        machines = Machine.objects.all().values('id').order_by('id')

        queue_name = ''
        for i in machines:
            mid = int(i['id'])
            if mid in machines_ok:
                queue_name += '1'
            else:
                queue_name += '0'
        return queue_name


class SubmissionMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionMessage
        fields = '__all__'


class SubmissionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionDetail
        fields = '__all__'


class SubmissionCodeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionCode
        fields = '__all__'
