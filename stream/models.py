from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

import model_utils.fields as util_fields


class Technology(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    description = models.TextField()
    visibility = (('public', _('Public')),
                  ('private', _('Private')))

    creator = models.ForeignKey(User, null=True, blank=True)
    subscribers = models.ManyToManyField(User, related_name='subscribed_technologies')


class TechnologyMaterial(models.Model):
    url = models.URLField()
    description = models.TextField()

    technology = models.ForeignKey('Technology')
    creator = models.ForeignKey(User, null=True)


class StreamSeries(models.Model):
    name = models.CharField(max_length=100)
    created = util_fields.AutoCreatedField()
    github_repo = models.CharField(max_length=255)

    owner = models.ForeignKey(User, null=True, blank=True)
    technologies = models.ManyToManyField(Technology)
    subscribers = models.ManyToManyField(User, related_name='subscribed_streams')


class StreamQuerySet(models.QuerySet):
    def active(self):
        return self.filter(pk__in=ActiveStream.objects.values_list('stream_id', flat=True))


class StreamManager(models.Manager):
    def get_queryset(self):
        return StreamQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()


class Stream(models.Model):
    title = models.CharField(max_length=100)
    created = util_fields.AutoCreatedField()
    finished = models.DateTimeField(null=True, blank=True)

    owner = models.ForeignKey(User, null=True, blank=True)
    series = models.ForeignKey(StreamSeries, null=True, blank=True)
    technologies = models.ManyToManyField(Technology, null=True, blank=True)

    objects = StreamManager()


class ActiveStream(models.Model):
    stream = models.ForeignKey(Stream)


class Event(models.Model):
    title = models.CharField(max_length=255)
    # object = models.ForeignObject()