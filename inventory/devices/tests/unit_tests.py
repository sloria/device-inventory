from django.test import TestCase
from nose.tools import *

from inventory.devices.tests.factories import DeviceFactory
from inventory.devices.models import Device

class DeviceTest(TestCase):
    def test_model(self):
        device = Device.objects.create(name='iPad',
                                status='Checked in')
        assert_true(device.pk)
        assert_true(device.status)
