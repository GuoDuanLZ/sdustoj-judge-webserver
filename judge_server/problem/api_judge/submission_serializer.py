from rest_framework import serializers

from ..models import Submission, SubmissionDetail

from .submission_conf import result_priority, result_map


class StatusSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=8, write_only=True, allow_null=True)
    sid = serializers.CharField(max_length=32, write_only=True)
    tid = serializers.CharField(max_length=32, allow_null=True, write_only=True)
    status = serializers.CharField(max_length=32, write_only=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        sid = validated_data['sid']
        tid = validated_data.get('tid')
        status = validated_data['status']

        submission = Submission.objects.filter(id=int(sid)).first()
        if submission is None:
            raise serializers.ValidationError('submission not exists')

        if tid == 'NULL' or tid is None:
            submission.status = result_map[status] if status in result_map else 'Unknown Status'
            submission.machine = instance
            submission.save()
        else:
            detail = SubmissionDetail.objects.get(submission=submission)
            detail.info[int(tid)] = result_map[status] if status in result_map else 'Unknown Status'
            detail.save()
        return submission


class ResultSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=8, allow_null=True, write_only=True)
    sid = serializers.CharField(max_length=32, write_only=True)
    tid = serializers.CharField(max_length=32, allow_null=True, write_only=True)
    time = serializers.CharField(max_length=32, write_only=True, allow_null=True)
    mem = serializers.CharField(max_length=32, write_only=True, allow_null=True)
    clen = serializers.CharField(max_length=32, write_only=True, allow_null=True)
    ret = serializers.CharField(max_length=32, write_only=True)
    msg = serializers.CharField(write_only=True, allow_null=True)

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        sid = validated_data['sid']
        tid = validated_data.get('tid')
        time = validated_data.get('time')
        mem = validated_data.get('mem')
        clen = validated_data.get('clen')
        ret = validated_data['ret']
        msg = validated_data.get('msg')

        ret = result_map[ret] if ret in result_map else 'Unknown Result'

        submission = Submission.objects.filter(id=int(sid)).first()
        if submission is None:
            raise serializers.ValidationError('submission not exists')

        if tid == 'NULL' or tid is None:
            submission.status = ret
            submission.finished = True
            submission.machine = instance
            submission.save()
            submission.message.content = msg
            submission.message.save()
        else:
            detail = SubmissionDetail.objects.get(submission=submission)
            detail.info[str(int(tid))] = {
                'result': ret,
                'time': time,
                'memory': mem,
                'code_length': clen,
                'detail': msg
            }
            detail.save()
            status, finished = self._get_global_result(detail.info)
            submission.status = status
            submission.finished = finished
            submission.save()
        return submission

    @staticmethod
    def _get_global_result(info):
        cur_status = 'Accepted'
        cur_priority = result_priority['Accepted']
        finished = True

        for result in dict(info).values():
            if isinstance(result, dict):
                ret = result['result']
                priority = result_priority[ret] if ret in result_priority else result_priority['DEFAULT']
                if priority >= cur_priority:
                    cur_priority = priority
                    cur_status = ret
            elif finished:
                finished = False

        if (not finished) and cur_status != 'Accepted':
            return 'Running & Judging', False
        elif not finished:
            return 'Running & Judging', False
        else:
            return cur_status, True
