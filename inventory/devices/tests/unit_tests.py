'''Unit tests for the devices models.'''

from django.test import TestCase
from nose.tools import *

from inventory.devices.models import Device
from inventory.devices.tests.factories import IpadFactory, create_device_factories


class DeviceTest(TestCase):
    def test_model(self):
        device = IpadFactory()
        assert_true(device.pk)
        assert_true(device.status)
        assert_true(device.created_at)
        assert_true(device.updated_at)
        assert_false(device.lendee)
        assert_false(device.lender)

    def test_saving_to_database(self):
        assert_equal(Device.objects.all().count(), 0)
        IpadFactory()
        assert_equal(Device.objects.all().count(), 1)


class FactoryTest(TestCase):
    def test_create_device_factories(self):
        ipad, headphones, adapter, case = create_device_factories()
        assert_in('ipad', ipad.make.lower())
        assert_in('headphones', headphones.make.lower())
        assert_in('adapter', adapter.make.lower())
        assert_in('case', case.make.lower())
