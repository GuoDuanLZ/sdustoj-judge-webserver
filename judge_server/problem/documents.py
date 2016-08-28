import mongoengine

from judge_server.conf_parser import TEST_DATA_READ_MAX


def get_mongodb_data(document, **kwargs):
    return getattr(document, 'objects').filter(**kwargs).first()


def write(target, source, chunk_size=512):
    while True:
        c = source.read(chunk_size)
        if c:
            target.write(c)
        else:
            break


class TestData(mongoengine.Document):
    tid = mongoengine.StringField(max_length=32, unique=True)
    mid = mongoengine.StringField(max_length=32)
    fin = mongoengine.FileField()
    fout = mongoengine.FileField()

    meta = {
        'indexes': [
            'mid',
            {
                'fields': ['tid'],
                'unique': 'True'
            },
        ]
    }

    @staticmethod
    def get_data(mid, tid):
        test_data = get_mongodb_data(TestData, mid=mid, tid=tid)
        if test_data is None:
            return '', ''
        file_in = test_data.fin.read(TEST_DATA_READ_MAX)
        file_out = test_data.fout.read(TEST_DATA_READ_MAX)
        return file_in, file_out

    @staticmethod
    def set_data(mid, tid, test_in=False, test_out=False):
        test_data = get_mongodb_data(TestData, mid=mid, tid=tid)
        if test_data is None:
            test_data = TestData(mid=mid, tid=tid)
        if test_in is not False:
            test_data.fin = test_in
        if test_out is not False:
            test_data.fout = test_out
        test_data.save()

    @staticmethod
    def write_data(mid, tid, test_in=False, test_out=False):
        test_data = get_mongodb_data(TestData, mid=mid, tid=tid)
        if test_data is None:
            test_data = TestData(mid=mid, tid=tid)
        if test_in is not False:
            if test_in is None:
                test_data.fin = None
            else:
                test_data.fin.new_file()
                write(test_data.fin, test_in)
                test_data.fin.close()
        if test_out is not False:
            if test_out is None:
                test_data.fout = None
            else:
                test_data.fout.new_file()
                write(test_data.fout, test_out)
                test_data.fout.close()
        test_data.save()

    @staticmethod
    def remove_data(mid, tid):
        test_data = get_mongodb_data(TestData, mid=mid, tid=tid)
        if test_data is None:
            return False
        test_data.delete()
        return True


class CodeInfo(mongoengine.Document):
    sid = mongoengine.StringField(max_length=32)
    name = mongoengine.StringField(max_length=255)

    code = mongoengine.FileField()

    meta = {
        'indexed': [
            'sid',
            'name'
        ]
    }

    @staticmethod
    def get_code(sid, name):
        code_info = get_mongodb_data(CodeInfo, sid=sid, name=name)
        if code_info is None:
            return None
        code = code_info.code.read()
        return code

    @staticmethod
    def set_code(sid, name, code):
        code_info = get_mongodb_data(CodeInfo, sid=sid, name=name)
        if code_info is None:
            code_info = CodeInfo(sid=sid, name=name)
        code_info.code = code
        code_info.save()

    @staticmethod
    def remove_data(sid, name):
        code_info = get_mongodb_data(CodeInfo, sid=sid, name=name)
        if code_info is None:
            return False
        code_info.delete()
        return True


class SpecialJudge(mongoengine.Document):
    pid = mongoengine.StringField(max_length=32)
    mid = mongoengine.StringField(max_length=32)
    code = mongoengine.FileField()

    @staticmethod
    def get_code(pid):
        special_judge = get_mongodb_data(SpecialJudge, pid=pid)
        if special_judge is None:
            return None
        code = special_judge.code.read()
        return code

    @staticmethod
    def set_code(mid,pid,code):
        special_judge= get_mongodb_data(SpecialJudge, mid=mid, pid=pid)
        if special_judge is None:
            special_judge = SpecialJudge(mid=mid, pid=pid)
        special_judge.code = code
        special_judge.save()

    @staticmethod
    def remove_code(pid):
        special_judge = get_mongodb_data(SpecialJudge, pid=pid)
        if special_judge is None:
            return False
        special_judge.delete()
        return True