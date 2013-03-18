'''Unit tests for the devices models.'''

from django.test import TestCase
from nose.tools import *

from inventory.devices.models import Device
from inventory.devices.tests.factories import DeviceFactory

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
