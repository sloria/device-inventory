from django_webtest import WebTest
import unittest
from nose.tools import *
from inventory.user.tests.factories import ReaderFactory
from inventory.devices.tests.factories import DeviceFactory

class TestAReader(WebTest):
    def setUp(self):
        self.reader = ReaderFactory()

    def test_can_login(self):
        user = self.reader.user
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
        # i'm an reader, so I can't create a user
        assert_not_in('Create user', res)

    def test_cannot_create_device(self):
        # goes to root (logged in)
        res = self.app.get('/', user=self.reader.user).follow()
        # at the devices page
        assert_equal(res.request.path, '/devices/')
        # there's no Add device button
        assert_not_in('Add device', res)

        # tries to go directly to the add device page
        res = self.app.get('/devices/add/', user=self.reader.user).follow()
        # sees a not authorized warning
        assert_in('Forbidden', res)

    def test_can_see_devices(self):
        # a device is already created
        device = DeviceFactory()
        # goes to the device index
        res = self.app.get('/', user=self.reader.user).follow()
        # sees the device name
        res.mustcontain(device.name, device.get_status_display(), device.serial_number)

    def test_cannot_remove_device(self):
        # a device is created
        DeviceFactory()
        # goes to devices page
        res = self.app.get('/', user=self.reader.user).follow()
        # cannot select 'Delete device' (raises ValuError)
        form = res.forms['device_control']
        with assert_raises(ValueError):
            form['action'] = 'delete_selected'

    def test_cannot_checkout_device(self):
        # a device is created
        DeviceFactory()
        # goes to devices page
        res = self.app.get('/', user=self.reader.user).follow()
        # cannot select 'Delete device' (raises ValuError)
        form = res.forms['device_control']
        with assert_raises(ValueError):
            form['action'] = 'checkout_selected'

    def test_cannot_create_users(self):
        # logs in 
        res = self.app.get('/', user=self.reader.user).follow()
        assert_not_in('Create user', res)