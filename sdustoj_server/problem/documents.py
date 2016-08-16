import mongoengine


class TestData(mongoengine.Document):
    tid = mongoengine.StringField(max_length=32, unique=True)
    mid = mongoengine.StringField(max_length=32)
    fin = mongoengine.FileField()
    fout = mongoengine.FileField()
