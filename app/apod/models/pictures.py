import datetime
import mongoengine as me


# Based on: https://flask-mongoengine.readthedocs.org/en/latest/

class Post(me.Document):
	title = me.StringField(required=True)
	explanation = me.StringField()
	url = me.StringField()
	media_type = me.StringField()
	concepts = me.ListField()
    picture_date = me.DateTimeField(required=True)
    published = me.BooleanField(required=True)

    # TODO: make sure this is what we want. It's based on the MongoEngine docs.
    # Doesn't seem to work
    #@me.queryset_manager
    #def live_posts(doc_cls, queryset):
        #return queryset.filter(published=True)

