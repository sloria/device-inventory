'''Functional tests for the superuser user type'''

from django.contrib.auth.models import User
from django_webtest import WebTest
from nose.tools import *
from inventory.user.tests.factories import (UserFactory,
                                             LendeeFactory)
from inventory.devices.tests.factories import IpadFactory
from inventory.devices.models import *
from inventory.user.models import Experimenter, Reader

class TestASuperUser(WebTest):
    def setUp(self):
        self.admin = UserFactory(first_name="Alan", last_name="Admin")
        self.admin.is_superuser = True
        self.admin.save()

    def tearDown(self):
        pass

    def test_can_add_ipad(self):
        # Goes to root (already logged in)
        res = self.app.get('/', user=self.admin).follow()
        assert_equal(res.request.path, '/devices/')
        # There's an Add device button
        assert_in('Add device', res)
        res = res.click('Add device')
        assert_equal(res.request.path, '/devices/add/')
        assert_in('Add device', res)

        # Fills in form
        form = res.forms['device_form']
        form.set('device_type', 'ipad')  # selects iPad
        form['description'] = '16GB, white'
        # forgets to put make
        # submits
        res = form.submit()
        # error message is displayed
        assert_in('This field is required', res)
        # enters serial number
        form['make'] = 'SERW09302 iPad 4'
        # submits
        res = form.submit().follow()
        # device is saved to database
        assert_equal(Ipad.objects.all().count(), 1)
        assert_equal(Ipad.objects.latest().description,
                    '16GB, white')
        # redirected to device index
        assert_equal(res.request.path, '/devices/')
        # the new device's name, status, Lender/Lendee, serial number is displayed
        # headers
        res.mustcontain('Name', 'Lender', 'Lent to', 'Serial number', 'Updated at')
        res.mustcontain('iPad', 'Checked in - NOT READY')

    def test_can_add_headphones(self):
        # goes to add device page
        res = self.app.get('/devices/add/', user=self.admin)
        form = res.forms['device_form']
        form.set('device_type', 'headphones')  # selects headphones
        form['description'] = 'iPad headphones'
        form['make'] = 'iPad headphones'
        # submits
        res = form.submit().follow()
        # saved to db
        headphones = Headphones.objects.latest()
        assert_equal(headphones.name, 'Headphones')
        # redirected to device index
        assert_equal(res.request.path, '/devices/')

    def test_can_add_adapter(self):
        # goes to add device page
        res = self.app.get('/devices/add/', user=self.admin)
        # fills out the device form
        form = res.forms['device_form']
        form.set('device_type', 'adapter')  # selects adapter
        form['description'] = 'wall charger/adapter for iPad'
        form['make'] = "Apple wall charger adapter"
        # submits
        res = form.submit().follow()
        # saved to db
        adapter = Adapter.objects.latest()
        assert_in('adapter', adapter.make.lower())
        # redirected to device indes
        assert_equal(res.request.path, '/devices/')

    def test_can_add_case(self):
        # goes to add device page
        res = self.app.get('/devices/add/', user=self.admin)
        # fills out the device form
        form = res.forms['device_form']
        form.set('device_type', 'case')  # selects adapter
        form['description'] = 'case for iPad (blue)'
        form['make'] = "iPad Smartcase"
        # submits
        res = form.submit().follow()
        # saved to db
        case = Case.objects.latest()
        assert_in('case', case.make.lower())
        # redirected to device indes
        assert_equal(res.request.path, '/devices/')

    def test_can_see_delete_btn(self):
        # 3 devices are created
        device1, device2, device3 = IpadFactory(), IpadFactory(), IpadFactory()
        assert_equal(Ipad.objects.all().count(), 3)
        # user goes to index page
        res = self.app.get('/', user=self.admin).follow()
        # devices are listed
        assert_in(device1.serial_number, res)
        assert_in(device2.serial_number, res)
        # there is a delete button
        assert_in('Delete', res)

    def test_can_create_experimenter(self):
        # logs in 
        res = self.app.get('/', user=self.admin).follow()
        # Clicks on create new user
        res = res.click('Create user')
        # Fills out form to create a new user
        form = res.forms['user_form']
        # Sets the user type
        form.set('user_type', 'experimenter')
        form['first_name'] = 'Jimmy'
        form['last_name'] = 'Page'
        form['email'] = 'jimmy@example.com'
        form['password1'] = 'ledzep12'
        form['password2'] = 'ledzep12'
        # Submits
        res = form.submit().follow()
        # Back at the devices page
        assert_equal(res.request.path, '/devices/')
        # Sees success message
        assert_in('Successfully created user: jimmy@example.com', res)
        # User is saved to database
        assert_equal(Experimenter.objects.all().count(), 1)
        new_experimenter = Experimenter.objects.get(user__username='jimmy@example.com')
        assert_equal(new_experimenter.user.get_full_name(), 'Jimmy Page')

    def test_can_create_reader(self):
        # logs in 
        res = self.app.get('/', user=self.admin).follow()
        # Clicks on create new user
        res = res.click('Create user')
        # Fills out form to create a new user
        form = res.forms['user_form']
        # Sets the user type
        form.set('user_type', 'reader')
        form['first_name'] = 'Jimmy'
        form['last_name'] = 'Page'
        form['email'] = 'jimmy@example.com'
        form['password1'] = 'ledzep12'
        form['password2'] = 'ledzep12'
        # Submits
        res = form.submit().follow()
        # Back at the devices page
        assert_equal(res.request.path, '/devices/')
        # Sees success message
        assert_in('Successfully created user: jimmy@example.com', res)
        # User is saved to database
        assert_equal(Reader.objects.all().count(), 1)
        new_reader = Reader.objects.get(user__username='jimmy@example.com')
        assert_equal(new_reader.user.get_full_name(), 'Jimmy Page')

    def test_can_create_admin(self):
        # logs in 
        res = self.app.get('/', user=self.admin).follow()
        # Clicks on create new user
        res = res.click('Create user')
        # Fills out form to create a new user
        form = res.forms['user_form']
        # Sets the user type
        form.set('user_type', 'admin')
        form['first_name'] = 'Jimmy'
        form['last_name'] = 'Page'
        form['email'] = 'jimmy@example.com'
        form['password1'] = 'ledzep12'
        form['password2'] = 'ledzep12'
        # Submits
        res = form.submit().follow()
        # Back at the devices page
        assert_equal(res.request.path, '/devices/')
        # Sees success message
        assert_in('Successfully created user: jimmy@example.com', res)
        # User is saved to database
        new_admin = User.objects.get(username='jimmy@example.com')
        assert_equal(new_admin.get_full_name(), 'Jimmy Page')
        assert_true(new_admin.is_superuser)

    def test_can_delete_device(self):
        assert False, 'finish me'
