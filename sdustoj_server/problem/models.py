from utils.models import ModifyInfo, Resource, SourceMixin, StatusMixin
from django.db import models

from .documents import TestData as TestDataMongo
from sdustoj_server.conf_parser import TEST_DATA_READ_MAX

from judge.models import Environment


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
            self.mongo_data = TestDataMongo(tid=str(self.id), mid=str(self.meta_problem_id))
            self.mongo_data.save()
            data = self.mongo_data
        data.fin = test_in.encode('utf-8')
        data.save()

    def set_test_out(self, test_out):
        data = self.get_mongo_data()
        if data is False:
            self.mongo_data = TestDataMongo(tid=str(self.id), mid=str(self.meta_problem_id))
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


# ----- Components --------------------------------------------------------------------------------

class Limit(Resource, StatusMixin):
    problem = models.ForeignKey(to=Problem, related_name='limit', to_field='id')
    id = models.BigAutoField(primary_key=True)

    environment = models.ForeignKey(to=Environment, related_name='limit', to_field='id')

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
