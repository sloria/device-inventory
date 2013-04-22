'''Models for different kinds of users.'''

from django.db import models
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

class Subject(models.Model):
    '''A subject.
    '''
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    subject_id = models.IntegerField(max_length=200, null=False)

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
        content_type = ContentType.objects.get_for_model(Experimenter)
        change_status_perm, created = Permission.objects.get_or_create(
                                        name='Can change device status',
                                        codename='can_change_device_status',
                                        content_type=content_type
                                    )
        change_attributes_perm, created = Permission.objects.get_or_create(
                                        name='Can update device',
                                        codename='can_update_device_attributes',
                                        content_type=content_type
                                    )
        self.user.user_permissions.add(change_status_perm, change_attributes_perm)
        self.user.save()
        super(Experimenter, self).save()

    
    def get_last_name_first(self):
        return "{0}, {1}".format(self.user.last_name, self.user.first_name)

class Lendee(models.Model):
    '''A lendee. May either be a user or a subject (but not both).
    '''
    # TODO: shouldn't be able to have both a user and a subject. Rethink.
    user = models.OneToOneField(User, unique=True, null=True, blank=True)
    subject = models.OneToOneField(Subject, unique=True, null=True, blank=True)

    def __unicode__(self):
        return unicode(self.user)

    def get_last_name_first(self):
        '''Returns as string with the lendee's last name, a comma, then their
        first name.

        Example: Hooker, John
        '''
        if self.user:
            return "{0}, {1}".format(self.user.last_name, self.user.first_name)
        else:
            return "{0}, {1}".format(self.subject.last_name, self.subject.first_name)

class Reader(models.Model):
    '''A reader. Can only view devices (cannot add/delete/change/status).
    '''
    user = models.OneToOneField(User, unique=True)

    def __unicode__(self):
        return unicode(self.user)