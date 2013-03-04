from django.test import TestCase
from nose.tools import *

from inventory.devices.tests.factories import DeviceFactory
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
