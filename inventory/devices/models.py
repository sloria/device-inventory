'''Models for the devices app.'''

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from inventory.user.models import Lendee
 
class Device(models.Model):
    '''A device.
    '''
    # These constants define choices for a device's status
    CHECKED_IN = 'CI'
    CHECKED_OUT = 'CO'
    STORAGE = 'ST'
    BROKEN = 'BR'
    MISSING = 'MI'

    # Other constants for condition
    EXCELLENT = 'EX'
    SCRATCHED = 'SC'

    # Define possible choices for Status field
    STATUS_CHOICES = (
        (CHECKED_IN, 'Checked in'),
        (CHECKED_OUT, 'Checked out'),
        (STORAGE, 'Storage'),
        (BROKEN, 'Broken'),
        (MISSING, 'Missing'),
    )

    # Define possible choices for condition field
    CONDITION_CHOICES = (
        (EXCELLENT, 'Excellent'),
        (SCRATCHED, 'Scratched'),
        (BROKEN, 'Broken'),
        (MISSING, 'Missing'),
    )

    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    responsible_party = models.CharField(max_length=100, null=True, blank=True)
    make = models.CharField(max_length=200)
    serial_number = models.CharField(max_length=200, unique=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=STORAGE)
    condition = models.CharField(max_length=2, choices=CONDITION_CHOICES, default=EXCELLENT)
    purchased_at = models.DateTimeField('Date purchased', default=timezone.now())
    created_at = models.DateTimeField('created at', default=timezone.now())
    updated_at = models.DateTimeField('updated at', default=timezone.now())
    lendee = models.ForeignKey(Lendee, null=True, blank=True, unique=False)
    lender = models.ForeignKey(User, null=True, blank=True, unique=False, related_name='lenders')

    def __unicode__(self):
        return unicode("name: {0}, status: {1}".format(self.name, self.status))

    def get_cname(self):
        return 'device'
        
    class Meta:
        permissions = (
            ('can_change_device_status', "Can change device status"),
            ('can_update_device_attributes', "Can update device attributes")
        )
        get_latest_by = 'created_at'
        ordering = ['-created_at', '-updated_at']

class Comment(models.Model):
    """A comment for a device. These are added when devices
    are checked in."""
    text = models.TextField(max_length=1000, null=False, blank=False)
    device = models.ForeignKey(Device, related_name='comments')
    user = models.ForeignKey(User, related_name='comments')
    created_at = models.DateTimeField('created at', default=timezone.now())
    updated_at = models.DateTimeField('updated at', default=timezone.now())

    def get_cname(self):
        return 'comment'


