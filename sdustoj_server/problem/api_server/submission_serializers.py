from rest_framework import serializers
from rest_framework.serializers import ValidationError

import redis
from sdustoj_server.redis_connections import pool as redis_pool

from sdustoj_server.conf_parser import MAX_OLEN
from json import dumps

from judge.models import Machine

from ..models import Submission, SubmissionTestInfo, SubmissionCode


class SubmitSerializer(serializers.ModelSerializer):
    code = serializers.CharField(write_only=True, style={'base_template': 'textarea.html'})

    class Meta:
        model = Submission
        fields = ('id', 'problem', 'environment', 'code')

    def create(self, validated_data):
        # 验证此题可交选择的环境
        problem = validated_data['problem']
        environment = validated_data['environment']
        if not problem.limit.filter(environment_id=environment.eid).exists():
            raise ValidationError('Problem does not support the language you choose.')

        # 获取提交上来的代码
        code = validated_data.pop('code')
        # 获取创建的提交实例
        instance = super().create(validated_data)

        # 创建提交记录对应的测试信息和代码文件
        self._create_test_info(problem, instance)
        self._create_code(instance, code)

        self._submit_to_queue(instance, code)

        return instance

    @staticmethod
    def _create_test_info(problem, instance):
        test_data = problem.test_data.all().values('id')
        test_index = {}
        for i in test_data:
            test_index[i['id']] = 'Pending'

        info = SubmissionTestInfo()
        info.submission = instance
        info.test_info = test_index
        info.save()

    @staticmethod
    def _create_code(instance, code):
        code_file = SubmissionCode.File('submission_' + str(instance.id), True, code)

        codes = SubmissionCode()
        codes.submission = instance
        codes.file = {code_file.name: code_file.to_dict()}
        codes.set_code(code_file.name, code)
        codes.save()

    @staticmethod
    def _submit_to_queue(instance, code):
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

        message = SubmitSerializer._generate_judge_info(instance, code)

        r = redis.Redis(connection_pool=redis_pool)
        r.rpush(queue_name, message)

    @staticmethod
    def _generate_judge_info(submission, code):
        problem = submission.problem
        meta_problem = problem.meta_problem
        test_data = problem.test_data.values('id')

        limit = problem.limit.filter(environment_id=submission.environment_id).first()

        message = {
            'isFiles': 'false',
            'sid': str(submission.id),
            'mid': str(meta_problem.id),
            'pid': str(problem.id),
            'eid': str(submission.environment_id),
            'tid': [str(i['id']) for i in test_data],

            'tl': str(limit.time_limit),
            'ml': str(limit.memory_limit),
            'ol': str(MAX_OLEN),
            'cl': str(limit.length_limit),

            'ttype': str(problem.test_type),
            'code': str(code),
        }

        return dumps(message)


class SubmissionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'


class SubmissionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'
