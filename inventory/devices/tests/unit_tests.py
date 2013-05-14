'''Unit tests for the devices models.'''

from nose.tools import *
from django.test import TestCase

from inventory.devices.models import *
from inventory.devices.tests.factories import (IpadFactory,
    HeadphonesFactory, create_device_factories)


class IpadTest(TestCase):
    def test_model(self):
        ipad = IpadFactory()
        assert_true(ipad.pk)
        assert_true(ipad.status)
        assert_true(ipad.created_at)
        assert_true(ipad.updated_at)
        assert_false(ipad.lendee)
        assert_false(ipad.lender)

    def test_saving_to_database(self):
        assert_equal(Ipad.objects.all().count(), 0)
        IpadFactory()
        assert_equal(Ipad.objects.all().count(), 1)

class HeadphonesTest(TestCase):
    def test_model(self):
        headphones = HeadphonesFactory()
        assert_true(headphones.pk)
        assert_true(headphones.status)
        assert_true(headphones.created_at)
        assert_true(headphones.updated_at)
        assert_false(headphones.lendee)
        assert_false(headphones.lender)

    def test_display_status(self):
        headphones = HeadphonesFactory(status=Device.CHECKED_IN)
        assert_equal(headphones.get_verbose_status(),
                    'Checked in')

class FactoryTest(TestCase):
    def test_create_device_factories(self):
        ipad, headphones, adapter, case = create_device_factories()
        assert_in('ipad', ipad.make.lower())
        assert_in('headphones', headphones.make.lower())
        assert_in('adapter', adapter.make.lower())
        assert_in('case', case.make.lower())

