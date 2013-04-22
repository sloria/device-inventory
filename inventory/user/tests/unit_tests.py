'''Unit tests for the user models.'''

from django.test import TestCase
from nose.tools import *
from inventory.user.tests.factories import UserFactory, ExperimenterFactory, ReaderFactory

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
        assert_true(self.user.has_perm('user.can_change_device_status'))

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
        assert_true(self.experimenter.user.has_perm('user.can_change_device_status'))

class ReaderTest(TestCase):
    def setUp(self):
        self.reader = ReaderFactory()

    def test_cannot_create_device(self):
        assert_false(self.reader.user.has_perm('devices.add_device'))

    def test_cannot_change_devices(self):
        assert_false(self.reader.user.has_perm('devices.delete_device'))

    def test_cannot_change_device_status(self):
        assert_false(self.reader.user.has_perm('user.can_change_device_status'))