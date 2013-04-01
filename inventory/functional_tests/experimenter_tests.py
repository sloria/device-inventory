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
        # cannot select 'Delete device' (raises ValuError)
        form = res.forms['device_control']
        with assert_raises(ValueError):
            form['action'] = 'delete_selected'

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

    def test_cannot_select_checkin_if_already_checked_in(self):
        assert False, 'finish me'

    
    def _checkout(self, device_index, lendee):
        '''Helper method for going to the device index, selecting a device,
        clicking checkout, then filling out and submitting the lendee form.'''
        # goes to devices page
        res = self.app.get('/', user=self.experimenter.user).follow()
        # checks the first device
        form = res.forms['device_control']
        form.set('device_select', True, index=device_index)
        # Selects Checkout device
        form.set('action', 'checkout_selected')
        # Submits
        res = form.submit().follow()
        # taken to a page with a list of lendees
        assert_in('Select Lendee', res)
        assert_in(lendee.get_last_name_first(), res)
        form = res.forms['lendee_select_form']
        # Selects the radio button for one of the lendees
        form['lendee_select'] = str(lendee.pk) # pk is the same as the form field value
        # Submits
        res = form.submit().follow()
        return res


    def test_can_checkout_device_to_user(self):
        # two devices are already created
        DeviceFactory(serial_number='123')
        DeviceFactory(serial_number='456')

        # There are two lendees
        user_lendee1 = UserFactory(username="lendee1", first_name='Lois', last_name='Lendee')
        user_lendee2 = UserFactory(username='lendee2', first_name='Louie', last_name='Lendee')
        lendee1 = LendeeFactory(user=user_lendee1)
        lendee2 = LendeeFactory(user=user_lendee2)
        assert_equal(Device.objects.all().count(), 2)

        # Checkout the first device
        res = self._checkout(0, lendee1)

        # Redirected to the devices page
        # The Lendee and Lender have been updated on the page and in the DB
        device = Device.objects.get(serial_number='123')
        assert_in('Lendee, Lois', res)
        assert_equal(device.lendee, lendee1)
        assert_equal(device.lender, self.experimenter.user)
        assert_equal(device.status, Device.CHECKED_OUT)
        # Can see the lendee's name
        assert_in("Experimenter, &nbsp;Ellen", res)

        # Now check out the other device
        res = self._checkout(1, lendee2)

    def test_cannot_checkout_multiple_devices(self):
        # two devices created
        DeviceFactory()
        DeviceFactory()
        res = self.app.get('/', user=self.experimenter.user).follow()
        # checks both devices
        # checks the first device
        form = res.forms['device_control']
        form.set('device_select', True, index=0)
        form.set('device_select', True, index=1)
        # Selects Checkout device
        form.set('action', 'checkout_selected')
        # Submits
        res = form.submit().follow()
        # An error message appears
        assert_in('Cannot check out more than one device at a time', res)

    def test_cannot_create_users(self):
        # logs in 
        res = self.app.get('/', user=self.experimenter.user).follow()
        assert_not_in('Create user', res)

    
    def _checkin(self, device_index, condition="excellent"):
        '''Helper method for checking in a device. Goes to index, 
        selects the device, selects "Check in", selects condition, 
        then submits. Returns the response after submitting the checkin form.
        '''
        res = self.app.get('/', user=self.experimenter.user).follow()
        # at the index page, there's a device that's checked out
        assert_in('Checked out', res)
        # selects the device
        form = res.forms['device_control']
        form.set('device_select', True, index=device_index)
        # Selects the Check In action
        form['action'] = 'checkin_selected'
        # submits
        res = form.submit().follow()
        # taken to a page with a form for checking in
        assert_in('checkin', res.request.path)
        form = res.forms['checkin_form']
        # Can select the condition of the device 
        assert_in('Condition: ', res)
        # selects Scratched
        form['condition'] = condition
        # submits
        res = form.submit().follow()
        return res

    def test_can_checkin_a_scratched_device(self):
        # A device is created
        device = DeviceFactory(status=Device.CHECKED_OUT)
        
        # user checks in the device
        res = self._checkin(0, 'scratched')

        # status is updated in database
        device = Device.objects.get(pk=device.pk)
        assert_equal(device.status, Device.CHECKED_IN)
        # condition is updated in database
        assert_equal(device.condition, Device.SCRATCHED)

        # The lendee's name should not be visible
        assert_not_in(self.experimenter.get_last_name_first(), res)
        # Sees success message
        assert_in('Successfully checked in', res)

    def test_can_checkin_a_broken_device(self):
        # device is created
        device = DeviceFactory(status=Device.CHECKED_OUT)

        # user checks in the device and changes condition to broken
        res = self._checkin(0, 'broken')
        # status is updated in database
        device = Device.objects.get(pk=device.pk)
        assert_equal(device.status, Device.BROKEN)
        # The lendee's name should not be visible because the device is checked in
        assert_not_in(self.experimenter.get_last_name_first(), res)
        # Sees success message
        assert_in('Successfully checked in', res)

    def test_checkout_with_no_lendees_and_creating_subject(self):
        # device is created 
        # note: there are no lendees
        device = DeviceFactory(status=Device.CHECKED_IN)
        # goes to homepage
        res = self.app.get('/', user=self.experimenter.user).follow()
        form = res.forms['device_control']
        # selects the device checkbox and chooses checkout
        form.set('device_select', True, 0) # select first (0-th) device
        form['action'] = 'checkout_selected'
        # submits
        res = form.submit().follow()
        # on the new page, there is text saying that there 
        # are no lendees
        assert_in('Nobody to lend to', res)
        # but there is a link to create a new lendee; clicks it
        res = res.click('Create new subject')
        # taken to a subject form
        form = res.forms['subject_form']
        # fills out the form
        form['first_name'] = 'Sally'
        form['last_name'] = 'Subject'
        form['subject_id'] = '1234ABC'
        # submits
        res = form.submit().follow()
        # Subject is saved to db. A new Lendee is also created
        assert_equal(Subject.objects.all().count(), 1)
        assert_equal(Lendee.objects.all().count(), 1)
        # taken back to checkout page
        assert_equal('/devices/{0}/checkout/'.format(device.pk), res.request.path)
        # Can now check out to the new subject
        res = self._checkout(0, Lendee.objects.all()[0]) # Checks out to the one and only Lendee
        # back to the index page
        assert_equal('/devices/', res.request.path)
        # change is saved to the db
        device = Device.objects.get(pk=device.pk) # Need to query device to get 
                                                    # The update attributes
        assert_equal(device.status, Device.CHECKED_OUT)
        assert_equal(device.lendee, Lendee.objects.all()[0])
        assert False, 'finish me (subject_id validation)'

    def test_can_change_device_condition(self):
        assert False, 'finish me'