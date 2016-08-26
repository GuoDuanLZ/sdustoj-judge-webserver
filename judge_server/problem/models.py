from utils.models import ModifyInfo, Resource, SourceMixin, StatusMixin
from django.db import models
from django.contrib.postgres import fields as postgres_fields

from .documents import TestData as TestDataMongodb

from judge.models import Environment, Machine
from client.models import Client


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
            test_in = data[0].decode('utf-8', 'ignore') if data[0] is not None else None
            test_out = data[1].decode('utf-8', 'ignore') if data[1] is not None else None
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


# ----- Components --------------------------------------------------------------------------------

class Limit(Resource, StatusMixin):
    problem = models.ForeignKey(to=Problem, related_name='limit', to_field='id')
    id = models.BigAutoField(primary_key=True)

    environment = models.ForeignKey(to=Environment, related_name='limit', to_field='eid')
    language = models.CharField(max_length=32, null=True)

    time_limit = models.IntegerField(default=-1)
    memory_limit = models.IntegerField(default=-1)
    length_limit = models.IntegerField(default=-1)


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
    content = models.TextField()


class SubmissionDetail(models.Model):
    submission = models.OneToOneField(to=Submission, related_name='detail', to_field='id', primary_key=True)
    info = postgres_fields.JSONField()


class SubmissionCode(models.Model):
    submission = models.OneToOneField(to=Submission, related_name='code', to_field='id', primary_key=True)
    info = postgres_fields.JSONField()
