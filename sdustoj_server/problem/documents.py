import mongoengine


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


class Code(mongoengine.Document):
    sid = mongoengine.StringField(max_length=32)
    name = mongoengine.StringField(max_length=255)

    code = mongoengine.FileField()

    meta = {
        'indexed': [
            'sid',
            'name'
        ]
    }
