import datetime
import mongoengine as me


# Based on: https://flask-mongoengine.readthedocs.org/en/latest/

class APIRecord(me.EmbeddedDocument):
    title = me.StringField(required=True)
    explanation = me.StringField()
    url = me.URLField()
    media_type = me.StringField()
    concepts = me.ListField(me.StringField())
    requested_date = me.DateTimeField(default=datetime.datetime.now)


class Picture(me.Document):
    apod_date = me.DateTimeField()
    api_record = me.ListField(me.EmbeddedDocumentField(APIRecord))
    published = me.BooleanField(required=True)
