from utils.models import ModifyInfo, Resource, SourceMixin, StatusMixin
from django.db import models

from .documents import TestData as TestDataMongo, Code as CodeMongo
from sdustoj_server.conf_parser import TEST_DATA_READ_MAX

from judge.models import Environment
from client.models import Client

from django.contrib.postgres import fields as postgres_fields


# Meta Problem #########################################################################################################

class MetaProblem(Resource, SourceMixin, StatusMixin):
    id = models.BigAutoField(primary_key=True)

    number_description = models.IntegerField(default=0)
    number_sample = models.IntegerField(default=0)
    number_test_data = models.IntegerField(default=0)
    number_virtual_judge = models.IntegerField(default=0)

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

    mongo_data = None
    test_in = None
    test_out = None

    def get_mongo_data(self):
        if self.mongo_data is None:
            self.mongo_data = TestDataMongo.objects.filter(tid=str(self.id)).first()
            if self.mongo_data is None:
                self.mongo_data = False
        return self.mongo_data

    def delete_mongo_data(self):
        if self.mongo_data is None:
            self.get_mongo_data()
        if self.mongo_data is not False:
            self.mongo_data.delete()

    def get_test_in(self):
        if self.test_in is not None:
            return self.test_in
        data = self.get_mongo_data()
        if data is False:
            self.test_in = ''
        else:
            read = data.fin.read(TEST_DATA_READ_MAX)
            if read is None:
                self.test_in = ''
            else:
                read = read.decode('utf-8')
                self.test_in = read
        return self.test_in

    def get_test_out(self):
        if self.test_out is not None:
            return self.test_out
        data = self.get_mongo_data()
        if data is False:
            self.test_out = ''
        else:
            read = data.fout.read(TEST_DATA_READ_MAX)
            if read is None:
                self.test_out = ''
            else:
                read = read.decode('utf-8')
                self.test_out = read
        return self.test_out

    def set_test_in(self, test_in):
        data = self.get_mongo_data()
        if data is False:
            self.mongo_data = TestDataMongo(tid=str(self.id), mid=str(self.id))
            self.mongo_data.save()
            data = self.mongo_data
        data.fin = test_in.encode('utf-8')
        data.save()

    def set_test_out(self, test_out):
        data = self.get_mongo_data()
        if data is False:
            self.mongo_data = TestDataMongo(tid=str(self.id), mid=str(self.id))
            self.mongo_data.save()
            data = self.mongo_data
        data.fout = test_out.encode('utf-8')
        data.save()

    def __str__(self):
        return 'TestData ' + str(self.id) + ': ' + str(self.title)


class VirtualJudge(Resource, StatusMixin):
    id = models.BigAutoField(primary_key=True)
    meta_problem = models.ForeignKey(to=MetaProblem, related_name='virtual_judge', to_field='id')

    number_problem = models.IntegerField(default=0)


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
    virtual_judge = models.ManyToManyField(to=VirtualJudge, related_name='problem',
                                           through='ProblemVirtualJudge', through_fields=('problem', 'virtual_judge'))

    number_test_data = models.IntegerField(default=0)
    number_virtual_judge = models.IntegerField(default=0)
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


class ProblemVirtualJudge(ModifyInfo):
    id = models.BigAutoField(primary_key=True)

    problem = models.ForeignKey(to=Problem, related_name='virtual_judge_relation', to_field='id',
                                on_delete=models.CASCADE)
    virtual_judge = models.ForeignKey(to=VirtualJudge, related_name='problem_relation', to_field='id',
                                      on_delete=models.CASCADE)


# Category #############################################################################################################

class Category(Resource, SourceMixin, StatusMixin):
    id = models.BigAutoField(primary_key=True)

    problem = models.ManyToManyField(to=Problem, related_name='category',
                                     through='ProblemCategoryNode', through_fields=('category', 'problem'))

    number_node = models.IntegerField(default=0)
    number_problem = models.IntegerField(default=0)


# ----- Components --------------------------------------------------------------------------------

class Node(Resource, StatusMixin):
    category = models.ForeignKey(to=Category, related_name='node', to_field='id')
    id = models.BigAutoField(primary_key=True)

    parent = models.ForeignKey(to='self', related_name='children', to_field='id', null=True)

    problem = models.ManyToManyField(to=Problem, related_name='node',
                                     through='ProblemCategoryNode', through_fields=('node', 'problem'))

    number_node = models.IntegerField(default=0)
    number_problem = models.IntegerField(default=0)


# ----- Relations ---------------------------------------------------------------------------------

class ProblemCategoryNode(ModifyInfo):
    category = models.ForeignKey(to=Category, related_name='problem_relation', to_field='id')
    problem = models.ForeignKey(to=Problem, related_name='node_relation', to_field='id')
    node = models.ForeignKey(to=Node, related_name='problem_relation', to_field='id')


# Submission ###########################################################################################################

class Submission(models.Model):
    RESULT_CHOICES = (
        ('PD', 'Pending'),
        ('RPD', 'Pending Rejudge'),
        ('DC', 'Decorating'),
        ('CP', 'Compiling'),
        ('RN', 'Running'),
        ('JG', 'Judging'),
        ('RJ', 'Running & Judging'),

        ('IW', 'Invalid Word'),
        ('RF', 'Restrained Function'),
        ('DF', 'Decoration Failed'),

        ('CLLE', 'Code Length Limit Exceeded'),
        ('CE', 'Compile Error'),

        ('AC', 'Accepted'),
        ('PE', 'Presentation Error'),
        ('WA', 'Wrong Answer'),
        ('TLE', 'Time Limit Exceeded'),
        ('MLE', 'Memory Limit Exceeded'),
        ('OLE', 'Output Limit Exceeded'),
        ('RE', 'Runtime Error'),

        ('SE', 'Submission Error'),
        ('UE', 'Unknown Error'),
    )
    RESULT_TYPE = (
        ('WT', 'Waiting'),
        ('AC', 'Correct'),
        ('NE', 'Network Error'),
        ('CE', 'Code Error'),
        ('RE', 'Running Error'),
        ('JE', 'Judging Error'),
        ('UE', 'Unknown Error'),
    )
    id = models.BigAutoField(primary_key=True)

    client = models.ForeignKey(to=Client, related_name='submission', to_field='name', null=True)
    user = models.CharField(max_length=128, null=True)
    extra = models.CharField(max_length=128, null=True)

    problem = models.ForeignKey(to=Problem, related_name='submission', to_field='id')
    environment = models.ForeignKey(to=Environment, related_name='submission', to_field='eid')
    language = models.CharField(max_length=32)

    result = models.CharField(max_length=4, choices=RESULT_CHOICES, default='PD')
    result_type = models.CharField(max_length=2, default='WT')

    memory = models.IntegerField(null=True)
    time = models.IntegerField(null=True)
    code_length = models.IntegerField(null=True)

    submit_time = models.DateTimeField(auto_now_add=True)
    last_judge_time = models.DateTimeField(auto_now=True)


class SubmissionTestInfo(models.Model):
    class TestInfo(object):
        def __init__(self, tid, result):
            self.tid = tid
            self.result = result

    id = models.BigAutoField(primary_key=True)

    submission = models.OneToOneField(to=Submission, related_name='test_info', to_field='id')
    test_info = postgres_fields.JSONField()


class SubmissionCode(models.Model):
    class File(object):
        def __init__(self, name='', is_code=False, file_str=None):
            self.name = name
            self.is_code = is_code
            self.file_str = file_str

        def to_dict(self):
            return {
                'name': self.name,
                'is_code': self.is_code,
            }

    id = models.BigAutoField(primary_key=True)

    submission = models.ForeignKey(to=Submission, related_name='code', to_field='id')
    file = postgres_fields.JSONField()

    mongo_data = None
    code = None

    def get_mongo_data(self, name):
        if self.mongo_data is None:
            self.mongo_data = CodeMongo.objects.filter(sid=str(self.submission_id), name=name).first()
            if self.mongo_data is None:
                self.mongo_data = False
        return self.mongo_data

    def get_code(self, name):
        if self.code is not None:
            return self.code
        data = self.get_mongo_data(name)
        if data is False:
            self.code = ''
        else:
            self.code = data.code.read()
            if self.code is None:
                self.code = ''
            else:
                self.code = self.code.decode('utf-8')
        return self.code

    def set_code(self, name, code):
        data = self.get_mongo_data(name)
        if data is False:
            self.mongo_data = CodeMongo(sid=str(self.submission_id), name=name)
            self.mongo_data.save()
            data = self.mongo_data
        data.code = code.encode('utf-8')
        data.save()
