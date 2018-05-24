from flask_mongoengine import MongoEngine
from mongoengine import queryset_manager
import mongoengine

from datetime import datetime

db = MongoEngine()

class Image(db.Document):
    name = db.StringField()
    image = db.ImageField(thumbnail_size=(100, 100, True))
    path =  db.StringField()
    url = db.StringField()
    time = db.DateTimeField(default=datetime.now)
    meta = {
        'ordering': ['time'],
        'strict': False,
    }

class User(db.Document):
    name = db.StringField(required=True, max_length=128)
    password = db.StringField(max_length=256)
    email = db.StringField(max_length=64)
    description = db.StringField(max_length=1024)
    tags = db.StringField(max_length=256)

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    # TypeError: ObjectId('552f41e56a85f00dd043406b') is not JSON serializable
    def get_id(self):
        return str(self.id)

    def __unicode__(self):
        return self.name

class Code(db.Document):
    code = db.StringField()
    des = db.StringField()
    published = db.BooleanField(default=False)
    pub_date = db.DateTimeField(default=datetime.now)
    category = db.StringField()




class Todo(db.Document):
    title = db.StringField(max_length=60)
    text = db.StringField()
    done = db.BooleanField(default=False)
    pub_date = db.DateTimeField(default=datetime.now)
    user = db.ReferenceField(User, required=False)

    # Required for administrative interface
    def __unicode__(self):
        return self.title


class Tag(db.Document):
    name = db.StringField(max_length=50)
    cata = db.StringField()
    des = db.StringField()

    def __unicode__(self):
        return self.name


class Comment(db.EmbeddedDocument):
    created_at = db.DateTimeField(default=datetime.now, required=True)
    body = db.StringField(verbose_name="Comment", required=True)
    author = db.StringField(verbose_name="Name", max_length=255, required=True)
    meta = {
        'ordering': ['-create_time'],
		'strict': False,
    }


post_status = ((0, 'draft'), (1, 'published'))


class Post(db.Document):
    title = db.StringField(required=True, max_length=64)
    content = db.StringField(required=True)
    #comments = db.ListField(db.EmbeddedDocumentField('Comment'))
    #images = db.ListField(db.EmbeddedDocumentField('Image'))
    tags = db.ListField(db.ReferenceField('Tag'),reverse_delete_rule=mongoengine.PULL)
    #status = db.IntField(required=True, choices=post_status)
    status = db.BooleanField(default=True)
    create_time = db.DateTimeField(default=datetime.now)
    modify_time = db.DateTimeField(default=datetime.now)
    inner = db.ListField(db.EmbeddedDocumentField(Comment))
    name = db.StringField(required=True, max_length=64)
    #lols = db.ListField(db.StringField(max_length=20))
    image = db.StringField()






    def __unicode__(self):
        return self.title

    meta = {
        'ordering': ['-create_time'],
		'strict': False,
		'indexes': [
        {'fields': ['$title', "$content"],
         'weights': {'title': 10, 'content': 2}
        }]
    }




class File(db.Document):
    name = db.StringField(max_length=20)
    data = db.FileField()
    path =  db.StringField(max_length=20)



class Review(db.Document):
    title = db.StringField(required=True, max_length=64)
    rate = db.StringField(render_kw={"placeholder": "Rate From 1 to 10"})
    content = db.StringField(required=True)
    #comments = db.ListField(db.EmbeddedDocumentField('Comment'))
    #images = db.ListField(db.EmbeddedDocumentField('Image'))
    tags = db.ListField(db.ReferenceField('Tag'),reverse_delete_rule=mongoengine.PULL)
    #status = db.IntField(required=True, choices=post_status)
    status = db.BooleanField(default=True)
    create_time = db.DateTimeField(default=datetime.now)
    modify_time = db.DateTimeField(default=datetime.now)
    inner = db.ListField(db.EmbeddedDocumentField(Comment))
    name = db.StringField(required=True, max_length=64)
    #lols = db.ListField(db.StringField(max_length=20))
    image = db.StringField()

    def __unicode__(self):
        return self.title

    meta = {
        'ordering': ['-create_time'],
		'strict': False,
		'indexes': [
        {'fields': ['$title', "$content"],
         'weights': {'title': 10, 'content': 2}
        }]
    }





