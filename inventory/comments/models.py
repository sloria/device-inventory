'''Models for the comments app.'''
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.urlresolvers import reverse

from inventory.devices.models import (Ipad, Headphones, 
                                    Adapter, Case)


class Comment(models.Model):
    """An abstract comment model. These are added when devices
    are checked in. Each device type has its own comment model
    that inherits from this class.
    """
    text = models.TextField(max_length=1000, null=False, blank=False)
    # device = models.ForeignKey(Ipad, related_name='comments')
    # user = models.ForeignKey(User, related_name='comments')
    created_at = models.DateTimeField('created at', default=timezone.now())
    updated_at = models.DateTimeField('updated at', default=timezone.now())

    class Meta:
        abstract = True
        get_latest_by = 'updated_at'
        ordering = ['-updated_at', '-created_at']

    def get_cname(self):
        return 'comment'


class IpadComment(Comment):
    device = models.ForeignKey(Ipad, null=False, blank=False,
                                related_name='comments')
    user = models.ForeignKey(User, related_name='ipad_comments')

    @property
    def edit_url(self):
        """Returns the url for the edit page for this comment."""
        return reverse('comments:ipad_edit', args=(self.device.pk, self.pk))

    @property
    def device_url(self):
        '''Returns the url for the detail page of this comment's device.'''
        return reverse('devices:ipad_detail', args=(self.device.pk,))

    def save(self, *args, **kwargs):
        # Update the updated_at field upon saving
        now = timezone.now()
        self.updated_at = now
        # Also update the updated_at field for the device
        self.device.updated_at = now
        return super(IpadComment, self).save(*args, **kwargs)


class HeadphonesComment(Comment):
    device = models.ForeignKey(Headphones, null=False, blank=False,
                                related_name='comments')
    user = models.ForeignKey(User, related_name='headphones_comments')

    @property
    def edit_url(self):
        """Returns the url for the edit page for this comment."""
        return reverse('comments:headphones_edit', args=(self.device.pk, self.pk))

    @property
    def device_url(self):
        '''Returns the url for the detail page of this comment's device.'''
        return reverse('devices:headphones_detail', args=(self.device.pk,))

    def save(self, *args, **kwargs):
        now = timezone.now()
        self.updated_at = now
        self.device.updated_at = now
        return super(HeadphonesComment, self).save(*args, **kwargs)


class AdapterComment(Comment):
    device = models.ForeignKey(Adapter, null=False, blank=False,
                                related_name='comments')
    user = models.ForeignKey(User, related_name='adapter_comments')

    @property
    def edit_url(self):
        """Returns the url for the edit page for this comment."""
        return reverse('comments:adapter_edit', args=(self.device.pk, self.pk))

    @property
    def device_url(self):
        '''Returns the url for the detail page of this comment's device.'''
        return reverse('devices:adapter_detail', args=(self.device.pk,))

    def save(self, *args, **kwargs):
        now = timezone.now()
        self.updated_at = now
        self.device.updated_at = now
        return super(AdapterComment, self).save(*args, **kwargs)


class CaseComment(Comment):
    device = models.ForeignKey(Case, null=False, blank=False,
                                related_name='comments')
    user = models.ForeignKey(User, related_name='case_comments')

    @property
    def edit_url(self):
        """Returns the url for the edit page for this comment."""
        return reverse('comments:case_edit', args=(self.device.pk, self.pk))

    @property
    def device_url(self):
        '''Returns the url for the detail page of this comment's device.'''
        return reverse('devices:case_detail', args=(self.device.pk,))

    def save(self, *args, **kwargs):
        now = timezone.now()
        self.updated_at = now
        self.device.updated_at = now
        return super(CaseComment, self).save(*args, **kwargs)
