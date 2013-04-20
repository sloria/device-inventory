'''Functional tests for an Experimenter User'''

from django_webtest import WebTest
from nose.tools import *
from inventory.user.tests.factories import (UserFactory, ExperimenterFactory,
                                             LendeeFactory)
from inventory.devices.tests.factories import DeviceFactory
from inventory.devices.models import Device
from inventory.user.models import Subject, Lendee

class TestAnExperimenter(WebTest):
    def setUp(self):
        user = UserFactory(first_name="Ellen", last_name="Experimenter")
        self.experimenter = ExperimenterFactory(user=user)

    def test_can_login(self):
        user = self.experimenter.user
        # goes to root (not logged in)
        res = self.app.get('/')
        form = res.forms['login_form']
        # fills in login info
        form['username'] = user.username
        form['password'] = 'abc'
        # submits
        res = form.submit().follow()
        # redirected to devices
        assert_equal(res.request.path, '/devices')
        assert_true(user.is_authenticated())
        # i'm an experimenter, so I can't create a user
        assert_not_in('Create user', res)

    def test_cannot_create_device(self):
        # goes to root (logged in)
        res = self.app.get('/', user=self.experimenter.user).follow()
        assert_equal(res.request.path, '/devices/')
        assert_not_in('Add device', res)
        # tries to go directly to the add device page
        res = self.app.get('/devices/add/', user=self.experimenter.user).follow()
        # sees a not authorized warning
        assert_in('Forbidden', res)

    def test_cannot_remove_device(self):
        # a device is created
        DeviceFactory()
        # goes to devices page
        res = self.app.get('/', user=self.experimenter.user).follow()
        # cannot see delete device
        assert_not_in('Delete', res)

    def test_can_see_devices(self):
        # a device is already created
        device = DeviceFactory()
        # goes to the device index
        res = self.app.get('/', user=self.experimenter.user).follow()
        # sees the device name
        res.mustcontain(device.name, 
                        device.get_status_display(), 
                        device.get_condition_display(),
                        device.serial_number)

    def test_cannot_create_users(self):
        # logs in 
        res = self.app.get('/', user=self.experimenter.user).follow()
        assert_not_in('Create user', res)