'''Functional tests using WebTest'''

from django_webtest import WebTest
import unittest
from nose.tools import *
from inventory.user.tests.factories import UserFactory
from inventory.devices.tests.factories import *
from inventory.devices.models import Device

class TestAUser(WebTest):

    def setUp(self):
        self.user = UserFactory()

    def tearDown(self):
        pass

    def test_can_see_homepage(self):
        # Rosie goes to homepage
        res = self.app.get('/')
        assert_equal(res.status_code, 200)
        assert_in('Inventory', res)

    def test_redirected_to_login_if_not_logged_in(self):
        res = self.app.get('/devices/')
        res = res.follow()
        assert_equal(res.status_code, 200)
        assert_equal(res.request.path, '/')

    def test_can_login(self):
        # Rosie goes to root
        res = self.app.get('/')
        # Rosie logs in
        form = res.forms['loginForm']
        form['username'] = self.user.username
        form['password'] = 'abc'
        res = form.submit()
        # Follow login
        res = res.follow()
        # Follow redirect to devices
        res = res.follow()
        assert_equal(res.status_code, 200)
        assert_true(self.user.is_authenticated())
        assert_in('Logged in as {}'.format(self.user.username), res)
        # Rosie is at the inventory page
        assert_equal(res.request.path, '/devices/')

    def test_root_redirects_to_inventory_if_logged_in(self):
        # Rosie is logged in
        # When she goes to the root, 
        res = self.app.get('/', user=self.user).follow()
        # She is taken to the inventory page
        assert_equal(res.request.path, '/devices/')

class TestAnExperimenter(WebTest):
    def setUp(self):
        self.experimenter = ExperimenterFactory()

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
        # cannot select 'Delete device' (raises ValuError)
        form = res.forms['deviceControl']
        with assert_raises(ValueError):
            form['action'] = 'delete_selected'

    def test_can_see_devices(self):
        # a device is already created
        device = DeviceFactory()
        # goes to the device index
        res = self.app.get('/', user=self.experimenter.user).follow()
        # sees the device name
        res.mustcontain(device.name, device.get_status_display(), device.serial_number)

    def test_can_checkout_device(self):
        # two devices are already created
        DeviceFactory(serial_number='123')
        DeviceFactory()

        user_lendee = UserFactory(username="lendee1", first_name='Lois', last_name='Lendee')
        lendee1 = LendeeFactory(user=user_lendee)
        assert_equal(Device.objects.all().count(), 2)
        # goes to devices page
        res = self.app.get('/', user=self.experimenter.user).follow()
        # checks the first device
        form = res.forms['deviceControl']
        form.set('device_select', True, index=0)
        # Selects Checkout device
        form.set('action', 'checkout_selected')
        # Submits
        res = form.submit().follow()
        # taken to a page with a list of lendees
        assert_in('Select Lendee', res)
        assert_in('Lendee, Lois', res)
        form = res.forms['lendee_select_form']
        # Selects the radio button for one of the lendees
        form['lendee_select'] = '1' # selects lendee with pk 1
        # Submits
        res = form.submit().follow()
        # Redirected to the devices page
        # The Lendee and Lender have been updated on the page and in the DB
        assert_in('Lendee, Lois', res)
        assert_in(self.experimenter.user.username, res)
        device = Device.objects.get(serial_number='123')
        assert_equal(device.lendee, lendee1)

    def test_cannot_checkout_multiple_devices(self):
        # two devices created
        DeviceFactory()
        DeviceFactory()
        res = self.app.get('/', user=self.experimenter.user).follow()
        # checks both devices
        # checks the first device
        form = res.forms['deviceControl']
        form.set('device_select', True, index=0)
        form.set('device_select', True, index=1)
        # Selects Checkout device
        form.set('action', 'checkout_selected')
        # Submits
        res = form.submit().follow()
        # An error message appears
        assert_in('Cannot check out more than one device at a time', res)

class TestASuperUser(WebTest):
    def setUp(self):
        self.admin = UserFactory()
        self.admin.is_superuser = True
        self.admin.save()

    def tearDown(self):
        pass

    def test_can_add_device(self):
        # Goes to root (already logged in)
        res = self.app.get('/', user=self.admin).follow()
        assert_equal(res.request.path, '/devices/')
        # There's an Add device button
        assert_in('Add device', res)
        res = res.click('Add device')
        assert_equal(res.request.path, '/devices/add/')
        assert_in('Add device', res)

        # Fills in form
        form = res.forms['deviceForm']
        form['name'] = 'iPad 4, 16GB, WiFi'
        form['description'] = 'This is an Apple product.'
        form['responsible_party'] = 'Freddy Douglass'
        form['make'] = 'SERW09302'
        # forgets to put serial number
        # submits
        res = form.submit()
        # error message is displayed
        assert_in('This field is required', res)
        # enters serial number
        form['serial_number'] = '12345X67'
        # submits
        res = form.submit().follow()
        # device is saved to database
        assert_equal(Device.objects.all().count(), 1)
        # redirected to device index
        assert_equal(res.request.path, '/devices/')
        # the new device's name, status, Lender/Lendee, serial number is displayed
        # headers
        res.mustcontain('Name', 'Status', 'Lender', 'Lendee', 'Serial number')
        res.mustcontain('iPad 4, 16GB, WiFi', 'Storage', '12345X67')


    def test_can_remove_devices(self):
        # 3 devices are created
        device1, device2, device3 = DeviceFactory(), DeviceFactory(), DeviceFactory()
        assert_equal(Device.objects.all().count(), 3)
        # user goes to index page
        res = self.app.get('/', user=self.admin).follow()
        # devices are listed
        assert_in(device1.serial_number, res)
        assert_in(device2.serial_number, res)
        # selects first two devices
        form = res.forms['deviceControl']
        form.set('device_select', True, index=0)
        form.set('device_select', True, index=1)
        # selects delete action
        form.set('action', 'delete_selected')
        # submits
        res = form.submit().follow()
        # devices no longer appear
        assert_not_in(device1.serial_number, res)
        assert_not_in(device2.serial_number, res)
        # a success alert appears
        assert_in('Successfully deleted 2 devices', res)
        # devices were deleted from database
        assert_equal(Device.objects.all().count(), 1)

    def test_can_create_users(self):
        # logs in 
        res = self.app.get('/', user=self.admin).follow()
        # Clicks on create new user
        res = res.click('Create user')
        assert False, 'finish me'


class TestAReader(WebTest):
    def setUp(self):
        self.reader = ReaderFactory()

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
        form = res.forms['deviceControl']
        with assert_raises(ValueError):
            form['action'] = 'delete_selected'

    def test_cannot_checkout_device(self):
        # a device is created
        DeviceFactory()
        # goes to devices page
        res = self.app.get('/', user=self.reader.user).follow()
        # cannot select 'Delete device' (raises ValuError)
        form = res.forms['deviceControl']
        with assert_raises(ValueError):
            form['action'] = 'checkout_selected'


