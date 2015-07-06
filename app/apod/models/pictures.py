import datetime
import mongoengine as me


# Based on: https://flask-mongoengine.readthedocs.org/en/latest/

class APIRecord(me.EmbeddedDocument):
    title = me.StringField(required=True)
    explanation = me.StringField()
    url = me.URLField()
    media_type = me.StringField()
    concepts = me.ListField(StringField())


requested_date = me.DateTimeField(required=True, default=datetime.datetime.now)


class Picture(me.Document):
    apod_date = me.DateTimeField()
    api_record = me.StringField(EmbeddedDocumentField(APIRecord))
    published = me.BooleanField(required=True)
