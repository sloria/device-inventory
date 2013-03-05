'''Models for the devices app.'''

from django.db import models
from django.contrib.auth.models import User, Permission
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

class Experimenter(models.Model):
    '''An experimenter.
    '''
    user = models.OneToOneField(User, unique=True)

    def __unicode__(self):
        return unicode(self.user)

    def save(self, *args, **kwargs):
        '''Add permission to change device status 
        before saving.'''
        change_status_permission = Permission.objects.get(
                                            codename='can_change_device_status'
                                    )
        self.user.user_permissions.add(change_status_permission)
        self.user.save()
        super(Experimenter, self).save()

class Lendee(models.Model):
    '''A lendee. May either be a user or a subject (but not both).
    '''
    # TODO: shouldn't be able to have both a user and a subject. Rethink.
    user = models.OneToOneField(User, unique=True, null=True, blank=True)
    subject = models.OneToOneField(Subject, unique=True, null=True, blank=True)

    def __unicode__(self):
        return unicode(self.user)

class Reader(models.Model):
    '''A reader. Can only view devices (cannot add/delete/change/status).
    '''
    user = models.OneToOneField(User, unique=True)

    def __unicode__(self):
        return unicode(self.user)
        
class Device(models.Model):
    '''A device.
    '''
    # These constants define choices for a device's status
    CHECKED_IN = 'CI'
    CHECKED_OUT = 'CO'
    STORAGE = 'ST'
    BROKEN = 'BR'
    MISSING = 'MI'
    STATUS_CHOICES = (
        (CHECKED_IN, 'Checked in'),
        (CHECKED_OUT, 'Checked out'),
        (STORAGE, 'Storage'),
        (BROKEN, 'Broken'),
        (MISSING, 'Missing'),
    )

    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    responsible_party = models.CharField(max_length=100, null=True, blank=True)
    make = models.CharField(max_length=200)
    serial_number = models.CharField(max_length=200)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=STORAGE)
    purchased_at = models.DateTimeField('Date purchased', default=timezone.now())
    created_at = models.DateTimeField('created at', default=timezone.now())
    updated_at = models.DateTimeField('updated at', default=timezone.now())
    lendee = models.OneToOneField(Lendee, null=True, blank=True)
    lender = models.OneToOneField(User, null=True, blank=True)

    def __unicode__(self):
        return unicode("name: {}, status: {}".format(self.name, self.status))

    class Meta:
        permissions = (
            ('can_change_device_status', "Can change device status"),
        )
