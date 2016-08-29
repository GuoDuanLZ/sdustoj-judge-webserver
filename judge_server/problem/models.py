from utils.models import ModifyInfo, Resource, SourceMixin, StatusMixin
from django.db import models
from django.contrib.postgres import fields as postgres_fields

from .documents import TestData as TestDataMongodb

from judge.models import Environment, Machine
from client.models import Client

from django.db import transaction

from json import loads
from .tasks import send_data_insert


# Meta Problem #########################################################################################################

class MetaProblem(Resource, SourceMixin, StatusMixin):
    id = models.BigAutoField(primary_key=True)

    number_description = models.IntegerField(default=0)
    number_sample = models.IntegerField(default=0)
    number_test_data = models.IntegerField(default=0)

    number_problem = models.IntegerField(default=0)

    def __str__(self):
        return 'MetaProblem ' + str(self.id) + ': ' + str(self.title)


# ----- Components --------------------------------------------------------------------------------

class Description(Resource, StatusMixin):
    id = models.BigAutoField(primary_key=True)
    meta_problem = models.ForeignKey(to=MetaProblem, related_name='description', to_field='id')

    content = models.TextField(null=True)

    number_problem = models.IntegerField(default=0)

    def __str__(self):
        return 'Description ' + str(self.id) + ': ' + str(self.title)


class Sample(Resource, StatusMixin):
    id = models.BigAutoField(primary_key=True)
    meta_problem = models.ForeignKey(to=MetaProblem, related_name='sample', to_field='id')

    content = models.TextField(null=True)

    number_problem = models.IntegerField(default=0)

    def __str__(self):
        return 'Sample ' + str(self.id) + ': ' + str(self.title)


class TestData(Resource, StatusMixin):
    id = models.BigAutoField(primary_key=True)
    meta_problem = models.ForeignKey(to=MetaProblem, related_name='test_data', to_field='id')

    in_size = models.IntegerField(default=0)
    out_size = models.IntegerField(default=0)

    number_problem = models.IntegerField(default=0)

    _test_data_mongodb = None

    def _get_test_data(self):
        if self._test_data_mongodb is None:
            data = TestDataMongodb.get_data(str(self.meta_problem_id),
                                            str(self.id))
            if data[0] is not None and isinstance(data[0], bytes):
                test_in = data[0].decode('utf-8', 'ignore')
            else:
                test_in = data[0]
            if data[1] is not None and isinstance(data[1], bytes):
                test_out = data[1].decode('utf-8', 'ignore')
            else:
                test_out = data[1]
            self._test_data_mongodb = (test_in, test_out)
        return self._test_data_mongodb

    def get_test_in(self):
        return self._get_test_data()[0]

    def get_test_out(self):
        return self._get_test_data()[1]

    def __str__(self):
        return 'TestData ' + str(self.id) + ': ' + str(self.title)


# Problem ##############################################################################################################

class Problem(Resource, SourceMixin, StatusMixin):
    TEST_TYPE_CHOICES = (
        ('normal', 'normal'),
        ('ignBlank', 'ignore blank'),
        ('ignPunct', 'ignore punctuation'),
        ('SPJ', 'special judge'),
    )

    meta_problem = models.ForeignKey(to=MetaProblem, related_name='problem', to_field='id')
    id = models.BigAutoField(primary_key=True)

    test_type = models.CharField(max_length=8, choices=TEST_TYPE_CHOICES, default='normal')

    description = models.ForeignKey(to=Description, related_name='problem', to_field='id', null=True)
    sample = models.ForeignKey(to=Sample, related_name='problem', to_field='id', null=True)

    test_data = models.ManyToManyField(to=TestData, related_name='problem',
                                       through='ProblemTestData', through_fields=('problem', 'test_data'))

    number_test_data = models.IntegerField(default=0)
    number_decorator = models.IntegerField(default=0)
    number_limit = models.IntegerField(default=0)
    number_category = models.IntegerField(default=0)
    number_node = models.IntegerField(default=0)

    def __str__(self):
        return 'Problem ' + str(self.id) + ' - ' + str(self.title)

    @staticmethod
    @transaction.atomic
    def create_new_problem(description, sample, limits, tests, test_type,
                           title, introduction, source, author, status):
        meta_problem = MetaProblem(title=title, introduction=introduction, source=source, author=author, status=status)
        meta_problem.save()
        description = Description(meta_problem=meta_problem, content=description)
        description.save()
        sample = Sample(meta_problem=meta_problem, content=sample)
        sample.save()

        count = 1
        test_mongo = []
        test_relation = []
        for test in tests:
            title = test.get('title', str(count))
            introduction = test.get('introduction')
            status = 1
            test_in = test.get('test_in')
            if test_in is not None:
                test_in = test_in.read()
            else:
                test_in = ''
            test_out = test.get('test_out')
            if test_out is not None:
                test_out = test_out.read()
            else:
                test_out = ''
            test_data = TestData(title=title, introduction=introduction, status=status,
                                 in_size=len(test_in), out_size=len(test_out))
            test_data.save()
            test_relation.append(test_data)
            test_mongo.append((meta_problem.id, test_data.id, test_in.encode('utf-8'), test_out.encode('utf-8')))

        problem = Problem(title=title, introduction=introduction, source=source, author=author, status=status,
                          meta_problem=meta_problem, test_type=test_type, description=description, sample=sample)
        problem.save()

        limits = loads(limits) if isinstance(limits, str) else limits
        for limit in limits:
            title = limit.get('title', str(count))
            introduction = limit.get('introduction')
            status = 1
            environment = Environment.objects.filter(eid=limit.get('environment')).first()
            language = environment.language
            time_limit = limit.get('time_limit', 1)
            memory_limit = limit.get('memory_limit', 1)
            length_limit = limit.get('length_limit', 1)

            limit = Limit(title=title, introduction=introduction, status=status,
                          environment=environment, language=language,
                          time_limit=time_limit, memory_limit=memory_limit, length_limit=length_limit,
                          problem=problem)

            limit.save()

        for test in test_relation:
            relation = ProblemTestData(problem=problem, test_data=test)
            relation.save()

        for (mid, tid, test_in, test_out) in test_mongo:
            TestDataMongodb.set_data(mid, tid, test_in, test_out)

        send_data_insert.delay(str(meta_problem.id))
        return problem


# ----- Components --------------------------------------------------------------------------------

class Limit(Resource, StatusMixin):
    problem = models.ForeignKey(to=Problem, related_name='limit', to_field='id')
    id = models.BigAutoField(primary_key=True)

    environment = models.ForeignKey(to=Environment, related_name='limit', to_field='eid')
    language = models.CharField(max_length=32, null=True)

    time_limit = models.IntegerField(default=-1)
    memory_limit = models.IntegerField(default=-1)
    length_limit = models.IntegerField(default=-1)


class InvalidWord(ModifyInfo):
    problem = models.ForeignKey(to=Problem, related_name='invalid_word', to_field='id')
    id = models.BigAutoField(primary_key=True)
    word = models.CharField(max_length=64)


class SpecialJudge(Resource):
    problem = models.OneToOneField(to=Problem, related_name='special_judge', to_field='id', primary_key=True)
    environment = models.ForeignKey(to=Environment, related_name='special_judge', to_field='eid')


# ----- Relations ---------------------------------------------------------------------------------

class ProblemTestData(ModifyInfo):
    id = models.BigAutoField(primary_key=True)

    problem = models.ForeignKey(to=Problem, related_name='test_data_relation', to_field='id',
                                on_delete=models.CASCADE)
    test_data = models.ForeignKey(to=TestData, related_name='problem_relation', to_field='id',
                                  on_delete=models.CASCADE)


# Category #############################################################################################################

class Category(Resource, SourceMixin, StatusMixin):
    id = models.BigAutoField(primary_key=True)

    problem = models.ManyToManyField(to=Problem, related_name='category',
                                     through='ProblemCategoryNode', through_fields=('category', 'problem'))

    number_node = models.IntegerField(default=0)
    number_problem = models.IntegerField(default=0)

    def __str__(self):
        return 'Category ' + str(self.id) + ': ' + str(self.title)


# ----- Components --------------------------------------------------------------------------------

class Node(Resource, StatusMixin):
    category = models.ForeignKey(to=Category, related_name='node', to_field='id')
    id = models.BigAutoField(primary_key=True)

    parent = models.ForeignKey(to='self', related_name='children', to_field='id', null=True)

    problem = models.ManyToManyField(to=Problem, related_name='node',
                                     through='ProblemCategoryNode', through_fields=('node', 'problem'))

    number_node = models.IntegerField(default=0)
    number_problem = models.IntegerField(default=0)

    def __str__(self):
        return 'Node ' + str(self.id) + ': ' + str(self.title)


# ----- Relations ---------------------------------------------------------------------------------

class ProblemCategoryNode(ModifyInfo):
    category = models.ForeignKey(to=Category, related_name='problem_relation', to_field='id')
    problem = models.ForeignKey(to=Problem, related_name='node_relation', to_field='id')
    node = models.ForeignKey(to=Node, related_name='problem_relation', to_field='id')


# Submission ###########################################################################################################

class Submission(models.Model):
    id = models.BigAutoField(primary_key=True)
    # submission information
    problem = models.ForeignKey(to=Problem, related_name='submission', to_field='id')
    environment = models.ForeignKey(to=Environment, related_name='submission', to_field='eid')
    submit_time = models.DateTimeField(auto_now_add=True)
    judge_time = models.DateTimeField(auto_now=True)
    code_length = models.IntegerField()
    # client information
    client = models.ForeignKey(to=Client, related_name='submission', to_field='id', null=True)
    user = models.CharField(max_length=64)
    contest = models.CharField(max_length=128, null=True)
    # status information
    finished = models.BooleanField(default=False)
    status = models.CharField(max_length=32, default='Pending')
    # judge information
    machine = models.ForeignKey(to=Machine, related_name='submission', to_field='name', null=True)


class SubmissionMessage(models.Model):
    submission = models.OneToOneField(to=Submission, related_name='message', to_field='id', primary_key=True)
    content = models.TextField(null=True)


class SubmissionDetail(models.Model):
    submission = models.OneToOneField(to=Submission, related_name='detail', to_field='id', primary_key=True)
    info = postgres_fields.JSONField()


class SubmissionCode(models.Model):
    submission = models.OneToOneField(to=Submission, related_name='code', to_field='id', primary_key=True)
    info = postgres_fields.JSONField()
