from django.test import TestCase
from django.contrib.auth.models import User
from nose.tools import *

from inventory.devices.tests.factories import *
from inventory.devices.models import Device

class DeviceTest(TestCase):
    def test_model(self):
        device = DeviceFactory()
        assert_true(device.pk)
        assert_true(device.status)
        assert_true(device.created_at)
        assert_true(device.updated_at)
        assert_false(device.lendee)
        assert_false(device.lender)

    def test_saving_to_database(self):
        assert_equal(Device.objects.all().count(), 0)
        DeviceFactory()
        assert_equal(Device.objects.all().count(), 1)

class AdminUserTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user.is_superuser = True
        self.user.save()

    def test_can_create_device(self):
        '''Superuser can create a device.'''
        assert_true(self.user.has_perm('devices.add_device'))

    def test_can_delete_device(self):
        assert_true(self.user.has_perm('devices.delete_device'))

    def test_can_change_device_status(self):
        assert_true(self.user.has_perm('devices.can_change_device_status'))

class ExperimenterTest(TestCase):
    def setUp(self):
        self.experimenter = ExperimenterFactory()

    def test_model(self):
        lender = ExperimenterFactory()
        assert_true(lender.user.pk)

    def test_cannot_create_device(self):
        '''Lenders cannot create devices.'''
        assert_false(self.experimenter.user.has_perm('devices.add_device'))

    def test_can_change_device_status(self):
        assert_true(self.experimenter.user.has_perm('devices.can_change_device_status'))

class ReaderTest(TestCase):
    def setUp(self):
        self.reader = ReaderFactory()

    def test_cannot_create_device(self):
        assert_false(self.reader.user.has_perm('devices.add_device'))

    def test_cannot_change_devices(self):
        assert_false(self.reader.user.has_perm('devices.delete_device'))

    def test_cannot_change_device_status(self):
        assert_false(self.reader.user.has_perm('devices.can_change_device_status'))
