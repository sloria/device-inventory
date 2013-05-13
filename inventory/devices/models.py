'''Models for the devices app.'''

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from inventory.user.models import Lendee


class Device(models.Model):
    '''An abstract device model.
    '''
    # These constants define choices for a device's status
    CHECKED_IN = 'CI'
    CHECKED_IN_READY = 'IR'
    CHECKED_IN_NOT_READY = 'IN'
    CHECKED_OUT = 'CO'
    STORAGE = 'ST'
    BROKEN = 'BR'
    MISSING = 'MI'
    SENT_FOR_REPAIR = 'RE'

    # Other constants for condition
    EXCELLENT = 'EX'
    SCRATCHED = 'SC'

    # Define possible choices for condition field
    CONDITION_CHOICES = (
        (EXCELLENT, 'Excellent'),
        (SCRATCHED, 'Scratched'),
        (BROKEN, 'Broken'),
        (MISSING, 'Missing'),
    )

    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000, null=True, blank=True)
    responsible_party = models.CharField(max_length=100, null=True, blank=True)
    make = models.CharField(max_length=200, null=False)
    purchased_at = models.DateTimeField('Date purchased', default=timezone.now())
    created_at = models.DateTimeField('created at', default=timezone.now())
    updated_at = models.DateTimeField('updated at', default=timezone.now())
    lendee = models.ForeignKey(Lendee, null=True, blank=True, unique=False)
    lender = models.ForeignKey(User, 
                            null=True, blank=True, unique=False)

    condition = models.CharField(max_length=2, 
                            choices=CONDITION_CHOICES, 
                            default=EXCELLENT)

    def __unicode__(self):
        return unicode("name: {0}, status: {1}".format(self.name, self.status))

    def get_verbose_status(self):
        '''Return a string with the status and the lendee, if
        the device is checked out.
        '''
        if self.status == Device.CHECKED_OUT:
            if self.lendee.user:
                return u'Checked out to {lendee}'\
                            .format(lendee=self.lendee.user.get_full_name())
            else:
                return u'Checked out to Subject {id}'\
                            .format(id=self.lendee.subject.subject_id)
        else:
            return self.get_status_display()

    def get_status_color(self):
        '''Return a css color that corresponds to the device's status.
        '''
        if self.status in [Device.CHECKED_IN_NOT_READY]:
            return 'red'
        elif self.status in [Device.CHECKED_IN_READY]:
            return 'green'
        elif self.status in [Device.CHECKED_OUT]:
            return '#ffcc00'

    def check_in(self, condition):
        """Checks in a device.
        """
        self.condition = condition
        self.status = Device.CHECKED_IN
        self.lendee = None
        self.lender = None
        return self.save()

    class Meta:
        abstract = True
        permissions = (
            ('can_change_device_status', "Can change device status"),
            ('can_update_device_attributes', "Can update device attributes")
        )
        get_latest_by = 'created_at'
        ordering = ['-updated_at', '-created_at']


class Ipad(Device):
    '''An Ipad.
    '''
    # Define possible choices for Status field
    STATUS_CHOICES = (
        (Device.CHECKED_IN_READY, 'Checked in - READY'),
        (Device.CHECKED_IN_NOT_READY, 'Checked in - NOT READY'),
        (Device.CHECKED_OUT, 'Checked out'),
        (Device.STORAGE, 'Storage'),
        (Device.BROKEN, 'Broken'),
        (Device.MISSING, 'Missing'),
        (Device.SENT_FOR_REPAIR, 'Sent for repair'),
    )

    serial_number = models.CharField(max_length=200, 
                                    null=True, blank=True, unique=False)

    status = models.CharField(max_length=2, 
                            choices=STATUS_CHOICES, 
                            default=Device.CHECKED_IN_NOT_READY)

    def save(self, *args, **kwargs):
        # If name isn't specified, set default name
        if not self.name:
            self.name = "iPad"
        self.updated_at = timezone.now()
        super(Ipad, self).save(*args, **kwargs)

    def check_in(self, condition):
        """Ipad-specific checkin method.
        Changes status to Checked in - NOT READY instead 
        of just CHECKED_IN.
        """
        self.condition = condition
        self.status = Device.CHECKED_IN_NOT_READY
        self.lendee = None
        self.lender = None
        return self.save()

    def get_cname(self):
        return 'ipad'

class Headphones(Device):
    '''Headphones model.
    '''
    # Define possible choices for Status field
    STATUS_CHOICES = (
        (Device.CHECKED_IN, 'Checked in'),
        (Device.CHECKED_OUT, 'Checked out'),
        (Device.STORAGE, 'Storage'),
        (Device.BROKEN, 'Broken'),
        (Device.MISSING, 'Missing'),
        (Device.SENT_FOR_REPAIR, 'Sent for repair'),
    )

    status = models.CharField(max_length=2, 
                            choices=STATUS_CHOICES, 
                            default=Device.CHECKED_IN)

    def save(self, *args, **kwargs):
        # If name isn't specified, set default name
        if not self.name:
            self.name = "Headphones"
        self.updated_at = timezone.now()
        super(Headphones, self).save(*args, **kwargs)

    def get_cname(self):
        return 'headphones'

class Adapter(Device):
    '''Adapter model.
    '''
    # Define possible choices for Status field
    STATUS_CHOICES = (
        (Device.CHECKED_IN, 'Checked in'),
        (Device.CHECKED_OUT, 'Checked out'),
        (Device.STORAGE, 'Storage'),
        (Device.BROKEN, 'Broken'),
        (Device.MISSING, 'Missing'),
        (Device.SENT_FOR_REPAIR, 'Sent for repair'),
    )

    status = models.CharField(max_length=2, 
                            choices=STATUS_CHOICES, 
                            default=Device.CHECKED_IN)

    def save(self, *args, **kwargs):
        # If name isn't specified, set default name
        if not self.name:
            self.name = "Power adapter"
        self.updated_at = timezone.now()
        super(Adapter, self).save(*args, **kwargs)

    def get_cname(self):
        return 'adapter'


class Case(Device):
    '''Case model.
    '''
    # Define possible choices for Status field
    STATUS_CHOICES = (
        (Device.CHECKED_IN, 'Checked in'),
        (Device.CHECKED_OUT, 'Checked out'),
        (Device.STORAGE, 'Storage'),
        (Device.BROKEN, 'Broken'),
        (Device.MISSING, 'Missing'),
        (Device.SENT_FOR_REPAIR, 'Sent for repair'),
    )

    status = models.CharField(max_length=2, 
                            choices=STATUS_CHOICES, 
                            default=Device.CHECKED_IN)

    def save(self, *args, **kwargs):
        # If name isn't specified, set default name
        if not self.name:
            self.name = "Case"
        self.update_at = timezone.now()
        super(Case, self).save(*args, **kwargs)

    def get_cname(self):
        return 'case'


class Comment(models.Model):
    """A comment for an iPad. These are added when iPads
    are checked in."""
    text = models.TextField(max_length=1000, null=False, blank=False)
    device = models.ForeignKey(Ipad, related_name='comments')
    user = models.ForeignKey(User, related_name='comments')
    created_at = models.DateTimeField('created at', default=timezone.now())
    updated_at = models.DateTimeField('updated at', default=timezone.now())

    class Meta:
        get_latest_by = 'updated_at'
        ordering = ['-updated_at', '-created_at']

    def get_cname(self):
        return 'comment'


