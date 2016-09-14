from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

from rest_framework.exceptions import NotFound, ValidationError

from .client_serializers import ClientSerializer, SubmissionSerializer
from ..models import Client
from problem.models import Problem, Category, Node, ProblemCategoryNode
from problem.models import SpecialJudge
from problem.models import Submission, SubmissionCode, SubmissionMessage, SubmissionDetail
from problem.documents import CodeInfo
from judge.models import Environment, Machine

from django.shortcuts import get_object_or_404

from datetime import datetime

from judge_server.redis_connections import pool
from redis import Redis
from judge_server.conf_parser import MAX_OLEN
from json import dumps


def is_valid_problem(client, problem):
    p_c = problem.node_relation.all().values('category_id').distinct()
    c_c = client.category.all().values('id')

    q = set()
    for i in c_c:
        q.add(i['id'])
    for i in p_c:
        if i['category_id'] in q:
            return True
    return False


def is_valid_category(client, category):
    return client.category.all().filter(id=category.id).exists()


class ClientViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    lookup_field = 'id_str'


class ProblemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Problem.objects.all()
    lookup_field = 'id'

    def list(self, request, *args, **kwargs):
        client = get_object_or_404(Client.objects.all(), id_str=kwargs['client_id_str'])
        categories = client.category.all()
        ret = []
        for cat in categories:
            cpns = cat.problem_relation.all()
            if 'min' in request.GET:
                cpns = cpns.filter(problem_id__gte=request.GET['min'])
            if 'max' in request.GET:
                cpns = cpns.filter(problem_id__lte=request.GET['max'])
            for cpn in cpns:
                problem = cpn.problem
                ret.append({
                    'id': problem.id,
                    'create_time': problem.create_time,
                    'update_time': problem.update_time,
                    'title': problem.title,
                    'introduction': problem.introduction,
                    'source': problem.source,
                    'author': problem.author,
                    'description': problem.description.content,
                    'sample': problem.sample.content,
                    'limits': problem.limit.values(
                        'environment', 'language', 'time_limit', 'memory_limit', 'length_limit'
                    )
                })
        return Response(ret)

    def retrieve(self, request, *args, **kwargs):
        client = get_object_or_404(Client.objects.all(), id_str=kwargs['client_id_str'])
        problem = get_object_or_404(Problem.objects.all(), id=kwargs['id'])

        if not is_valid_problem(client, problem):
            raise NotFound()

        ret = {
            'id': problem.id,
            'create_time': problem.create_time,
            'update_time': problem.update_time,
            'title': problem.title,
            'introduction': problem.introduction,
            'source': problem.source,
            'author': problem.author,
            'description': problem.description.content,
            'sample': problem.sample.content,
            'limits': problem.limit.values(
                'environment', 'language', 'time_limit', 'memory_limit', 'length_limit'
            )
        }

        return Response(ret)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    lookup_field = 'id'

    def list(self, request, *args, **kwargs):
        client = get_object_or_404(Client.objects.all(), id_str=kwargs['client_id_str'])
        categories = client.category.all().values(
            'id', 'create_time', 'update_time', 'title', 'introduction', 'source', 'author'
        )
        return Response(categories)

    def retrieve(self, request, *args, **kwargs):
        client = get_object_or_404(Client.objects.all(), id_str=kwargs['client_id_str'])
        category = get_object_or_404(Category.objects.all(), id=kwargs['id'])
        if not is_valid_category(client, category):
            raise NotFound()
        return Response({
            'id': category.id,
            'create_time': category.create_time,
            'update_time': category.update_time,
            'title': category.title,
            'introduction': category.introduction,
            'source': category.source,
            'author': category.source
        })


class NodeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Node.objects.all()
    lookup_field = 'id'

    def list(self, request, *args, **kwargs):
        client = get_object_or_404(Client.objects.all(), id_str=kwargs['client_id_str'])
        category = get_object_or_404(Category.objects.all(), id=kwargs['category_id'])
        if not is_valid_category(client, category):
            raise NotFound()
        return Response(category.node.all().values(
            'id', 'create_time', 'update_time', 'title', 'introduction', 'parent'
        ))

    def retrieve(self, request, *args, **kwargs):
        client = get_object_or_404(Client.objects.all(), id_str=kwargs['client_id_str'])
        category = get_object_or_404(Category.objects.all(), id=kwargs['category_id'])
        if not is_valid_category(client, category):
            raise NotFound()
        node = get_object_or_404(Node.objects.all(), id=kwargs['id'])
        return Response({
            'id': node.id,
            'create_time': node.create_time,
            'update_time': node.update_time,
            'title': node.title,
            'introduction': node.introduction,
            'parent': node.parent_id
        })


class CategoryProblemViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = ProblemCategoryNode.objects.all()

    def list(self, request, *args, **kwargs):
        client = get_object_or_404(Client.objects.all(), id_str=kwargs['client_id_str'])
        category = get_object_or_404(Category.objects.all(), id=kwargs['category_id'])
        if not is_valid_category(client, category):
            raise NotFound()
        q = ProblemCategoryNode.objects.filter(category=category)
        ret = []
        for i in q:
            ret.append({
                'pid': i.problem_id,
                'nid': i.node_id,
                'cid': i.category_id
            })
        return Response(ret)


class NodeProblemViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = ProblemCategoryNode.objects.all()

    def list(self, request, *args, **kwargs):
        client = get_object_or_404(Client.objects.all(), id_str=kwargs['client_id_str'])
        category = get_object_or_404(Category.objects.all(), id=kwargs['category_id'])
        if not is_valid_category(client, category):
            raise NotFound()
        node = get_object_or_404(Node.objects.all(), id=kwargs['node_id'])
        q = ProblemCategoryNode.objects.filter(node=node)
        ret = []
        for i in q:
            ret.append({
                'pid': i.problem_id,
                'nid': i.node_id,
                'cid': i.category_id
            })
        return Response(ret)


class SubmissionViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    lookup_field = 'id'

    def list(self, request, *args, **kwargs):
        client = get_object_or_404(Client.objects.all(), id_str=kwargs['client_id_str'])
        submissions = Submission.objects.filter(client=client)
        get = request.GET
        if 'min' in get:
            min_id = int(get['min'])
            submissions = submissions.filter(id__gte=min_id)
        if 'max' in get:
            max_id = int(get['max'])
            submissions = submissions.filter(id__lte=max_id)
        if 'min_time' in get:
            min_time = datetime.fromtimestamp(int(get['min_time']))
            submissions = submissions.filter(judge_time__gte=min_time)
        if 'max_time' in get:
            max_time = datetime.fromtimestamp(int(get['max_time']))
            submissions = submissions.filter(judge_time__gte=max_time)
        submissions = submissions[:2000]
        submissions = submissions.values(
            'id', 'problem', 'environment', 'submit_time', 'judge_time', 'code_length',
            'user', 'contest',
            'finished', 'status',
            'message__content',
            'detail__info',
        )
        ret = []
        for sub in submissions:
            sub['message'] = sub['message__content']
            sub['info'] = sub['detail__info']
            sub.pop('message__content')
            sub.pop('detail__info')
            ret.append(sub)
        return Response(ret)

    def create(self, request, *args, **kwargs):
        data = request.data
        if 'eid' not in data:
            raise ValidationError('eid required')
        if 'problem' not in data:
            raise ValidationError('problem required')
        if 'code' not in data:
            raise ValidationError('code required')
        if 'user' not in data:
            raise ValidationError('user required')

        client = get_object_or_404(Client.objects.all(), id_str=kwargs['client_id_str'])
        problem = get_object_or_404(Problem.objects.all(), id=data['problem'])
        if not is_valid_problem(client, problem):
            raise NotFound()
        environment = get_object_or_404(Environment.objects.all(), eid=data['eid'])
        limit = problem.limit.filter(environment=environment).first()
        if limit is None:
            raise ValidationError('environments selected not supported')

        code = data['code']
        user = data['user']

        submission = Submission()
        submission.problem = problem
        submission.environment = environment
        submission.code_length = len(code)
        submission.client = client
        submission.user = user
        if 'contest' in data:
            submission.contest = data['contest']
        submission.save()

        submission.code = SubmissionCode()
        submission.code.info = ['code']
        submission.code.save()
        submission.message = SubmissionMessage()
        submission.message.save()

        submission.detail = SubmissionDetail()
        submission.detail.info = {}
        test_data = submission.problem.test_data.all().values('id')
        for i in test_data:
            submission.detail.info[str(i['id'])] = '--'
        submission.detail.save()

        CodeInfo.set_code(str(submission.id), 'code', code.encode('utf-8'))

        r = Redis(connection_pool=pool)
        info = {
            'isFiles': 'false',
            'sid': str(submission.id),
            'mid': str(submission.problem.meta_problem_id),
            'pid': str(submission.problem_id),
            'eid': str(submission.environment_id),
            'tid': [str(i['id']) for i in test_data],
            'tl': str(limit.time_limit),
            'ml': str(limit.memory_limit),
            'cl': str(limit.length_limit),
            'ol': str(MAX_OLEN),
            'ttype': problem.test_type,
            'code': code,
        }

        special_judge = SpecialJudge.objects.filter(problem_id=submission.problem_id).first()
        if special_judge is not None:
            info['ttype'] = special_judge.environment_id

        invalid_words = ''
        for iw in problem.invalid_word.all():
            invalid_words += (' ' + iw.word)

        if invalid_words:
            invalid_words = invalid_words[1:]
            info['InvalidWord'] = invalid_words

        queue_name = self._get_queue_name(submission)
        info = dumps(info)
        print('sub to redis:', queue_name, info)

        r.rpush(queue_name, info)

        return Response(data='', status=status.HTTP_201_CREATED)

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
