from datetime import datetime
import mongoengine
from flask import g
from app import signals
from app.customqueryset import CustomQuerySet
from app.choices import CHOICES


class User(mongoengine.EmbeddedDocument):
    username = mongoengine.StringField()
    user_id = mongoengine.StringField()


class BaseDocument(mongoengine.Document):
    created_on = mongoengine.DateTimeField()
    modified_on = mongoengine.DateTimeField()
    status_modified_on = mongoengine.DateTimeField()
    created_by = mongoengine.EmbeddedDocumentField(User)
    modified_by = mongoengine.EmbeddedDocumentField(User)
    status_modified_by = mongoengine.EmbeddedDocumentField(User)
    is_active = mongoengine.BooleanField(default=False)
    inactive_reason = mongoengine.StringField()
    tags = mongoengine.ListField(mongoengine.StringField(choices=CHOICES["tags"]))

    meta = {
        'allow_inheritance': True,
        'abstract': True,
        'indexes': ['created_on', 'modified_on', 'is_active', 'tags'],
        'queryset_class': CustomQuerySet
     }

    def __str__(self):
        return str(self.uid)

    def save(self):
        current_datetime = datetime.now()
        if hasattr(self, 'created_on') and not self.created_on:
            self.created_on = current_datetime
            self.created_by = User(username=g.user_info['username'], user_id=g.user_info['user_id']) if hasattr(g, 'user_info') else User(username="default", user_id="0")
        self.modified_on = current_datetime
        self.modified_by = User(username=g.user_info['username'], user_id=g.user_info['user_id']) if hasattr(g, 'user_info') else User(username="default", user_id="0")

        if hasattr(self, '_changed_fields') and 'is_active' in self._changed_fields:
            self.status_modified_on = current_datetime
            self.status_modified_by = User(username=g.user_info['username'], user_id=g.user_info['user_id']) if hasattr(g, 'user_info') else User(username="default", user_id="0")
        return super().save()

    def update(self, **kwargs):
        current_datetime = datetime.now()
        kwargs['upsert'] = False  # upsert is set to false to make created_on and modified_on flag work properly
        kwargs['modified_on'] = current_datetime
        kwargs['modified_by'] = User(username=g.user_info['username'], user_id=g.user_info['user_id']) if hasattr(g, 'user_info') else User(username="default", user_id="0")
        if 'is_active' in kwargs:
            kwargs['status_modified_on'] = current_datetime
            kwargs['status_modified_by'] = kwargs['modified_by']
        return super().update(**kwargs)

    def update_and_signal(self, **values):
        signals.me_pre_update.send(self.__class__, **{'document': self, 'update': values})
        obj = self.update(**values)
        signals.me_post_update.send(self.__class__, **{'document': self, 'update': values})
        return obj

    @classmethod
    def create_or_update(cls, query, values):
        try:
            instance = cls.objects.get(**query)
        except mongoengine.DoesNotExist:
            instance = cls(**values)
            instance.save()
        else:
            instance.update(**values)
            instance.save()
        return instance

    @classmethod
    def create_or_update_and_signal(cls, query, values):
        try:
            instance = cls.objects.get(**query)
        except mongoengine.DoesNotExist:
            instance = cls(**values)
            signals.me_pre_update.send(instance.__class__, **{'document': instance})
            instance.save()
        else:
            signals.me_pre_update.send(instance.__class__, **{'document': instance, 'update': values})
            instance.update(**values)
            instance.save()
        signals.me_post_update.send(instance.__class__, **{'document': instance})
        return instance
