'''Functional tests using Selenium'''
import time
from nose.tools import *
from inventory.user.tests.factories import ExperimenterFactory, SubjectFactory
from inventory.devices.tests.factories import DeviceFactory
from inventory.devices.models import Device
from django.utils import timezone

from inventory.selenium_tests.utils import SeleniumTestCase, CustomWebDriver

class TestAnExperimenter(SeleniumTestCase):

    def setUp(self):
        # Create a user (Experimenter)
        self.experimenter = ExperimenterFactory()
        # Create a subject
        self.subject = SubjectFactory()
        # create a device
        self.device = DeviceFactory(status=Device.CHECKED_IN)
        self.driver = CustomWebDriver()
        self._login()

    def tearDown(self):
        self.driver.quit()

    def _login(self):
        self.open('/')
        self.driver.find_css('#id_username').\
                    send_keys(self.experimenter.user.username)
        self.driver.find_css('#id_password').send_keys('abc')
        self.driver.click_submit()

    def test_can_checkout_device_to_self(self):
        # at the device index page
        assert_in('Devices', self.driver.body_text())
        assert_not_in('12345', self.driver.body_text())
        # clicks on the table row for the device
        self.driver.find_css('tbody tr').click()
        # clicks check out
        self.driver.find_css('.btn-checkout').click()
        # a javascript input dialog pops up
        dialog = self.driver.switch_to_alert()
        assert_in(u'Check OUT - Enter a subject ID or user\'s e-mail address',
                dialog.text)
        # types in an invalid email address
        dialog.send_keys('notvalid@example.com')
        # clicks accept
        dialog.accept()
        time.sleep(1)  # wait for alert to come up
        # a dialog msg with an error appears
        dialog = self.driver.switch_to_alert()
        assert_in('No user found with e-mail address notvalid@example.com',
                    dialog.text)
        dialog.accept()  # Dismiss msg
        # clicks checkout again
        self.driver.find_css('.btn-checkout').click()
        dialog = self.driver.switch_to_alert()
        # types in user's email address
        dialog.send_keys(self.experimenter.user.username)
        # click accept
        dialog.accept()
        time.sleep(1)
        # a dialog appears
        dialog = self.driver.switch_to_alert()
        # it shows the lendee's name
        assert_in('Confirm check out to {name}?'.\
                format(name=self.experimenter.user.get_full_name()),
                dialog.text)
        dialog.accept()  # click accept
        time.sleep(2)
        # db record is updated
        device = Device.objects.get(pk=self.device.pk)
        assert_equal(device.status, Device.CHECKED_OUT)
        assert_equal(device.lendee.user.username,
                    self.experimenter.user.username)
        # updated status is shown on page
        assert_in('Successfully checked out', self.driver.body_text())
        assert_in(self.experimenter.user.get_full_name(), 
                    self.driver.body_text())

    def test_can_check_in(self):
        # There's a checked out device
        device = DeviceFactory(status=Device.CHECKED_OUT,
                                created_at=timezone.now(),
                                updated_at=timezone.now())
        self.open('/')
        # clicks on the table row for the checked IN device (second row)
        self.driver.find_css('tbody tr')[1].click()
        # clicks check in
        self.driver.find_css('.btn-checkin').click()
        # an alert dialog comes up saying that the device is already checked in
        dialog = self.driver.switch_to_alert()
        assert_in(u"Device is already checked in", dialog.text)
        # dismisses the alert
        dialog.accept()
        # clicks on the table row for the checked out device (top row)
        self.driver.find_css("tbody tr")[0].click()
        # clicks check in
        self.driver.find_css('.btn-checkin').click()
        # at the checkin page
        self.driver.click_submit()
        device = Device.objects.get(pk=device.pk)
        assert_equal(device.status, Device.CHECKED_IN)
        assert_in('Successfully checked in', self.driver.body_text())

    def test_can_checkout_device_to_subject(self):
        # clicks on the table row for the device
        self.driver.find_css('tbody tr').click()
        # clicks check out
        self.driver.find_css('.btn-checkout').click()
        # an dialog comes up
        dialog = self.driver.switch_to_alert()
        # enters an invalid subject ID
        dialog.send_keys("123")
        # clicks OK
        dialog.accept()
        # another dialog with an error message appears
        dialog = self.driver.switch_to_alert()
        assert_in(u"Invalid subject ID. Please try again.",
                    dialog.text)
        # dismisses the msg
        dialog.accept()
        # clicks checkout again
        self.driver.find_css('.btn-checkout').click()
        dialog = self.driver.switch_to_alert()
        # enters a valid subject ID
        dialog.send_keys("123451")
        dialog.accept()
        # a confirm msg comes up
        dialog = self.driver.switch_to_alert()
        assert_in('Confirm check out to Subject 123451?',
                            dialog.text)
        # clicks OK
        dialog.accept()
        time.sleep(2)
        # db record is updated
        device = Device.objects.get(pk=self.device.pk)
        assert_equal(device.status, Device.CHECKED_OUT)
        assert_equal(device.lendee.subject.subject_id, 123451)
        # updated status is shown on page
        assert_in('Successfully checked out', self.driver.body_text())
        assert_in("Subject: 123451", self.driver.body_text())
