'''Models for the devices app.'''

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Subject(models.Model):
    '''A subject.
    '''
    name = models.CharField(max_length=50, null=True, blank=True)
    subject_id = models.CharField(max_length=200)

    def validate_id(self):
        # TODO
        pass

    def __unicode__(self):
        return unicode(self.subject_id)

class Lender(models.Model):
    '''A lender.
    '''
    user = models.OneToOneField(User)
    def __unicode__(self):
        return unicode(self.name)


class Lendee(models.Model):
    '''A lendee. May either be a user or a subject (but not both).
    '''
    # TODO: shouldn't be able to have both a user and a subject. Rethink.
    user = models.OneToOneField(User, null=True, blank=True)
    subject = models.OneToOneField(Subject, null=True, blank=True)

    def __unicode__(self):
        return unicode(self.user)


class Device(models.Model):
    '''A device.
    '''
    name = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField('created at', default=timezone.now())
    updated_at = models.DateTimeField('updated at', default=timezone.now())
    lendee = models.OneToOneField(Lendee, null=True, blank=True)

    def __unicode__(self):
        return unicode("name: {}, status: {}".format(self.name, self.status))
