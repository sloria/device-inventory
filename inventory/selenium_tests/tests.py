'''Functional tests using Selenium'''
import time
from nose.tools import *
from inventory.user.tests.factories import ExperimenterFactory
from inventory.devices.tests.factories import DeviceFactory
from inventory.devices.models import Device

from inventory.selenium_tests.utils import SeleniumTestCase, CustomWebDriver

class TestAnExperimenter(SeleniumTestCase):

    def setUp(self):
        # Create a user (Experimenter)
        self.experimenter = ExperimenterFactory()
        # create a device
        self.device = DeviceFactory()
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
        time.sleep(3)
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
        # clicks on the table row for the device
        self.driver.find_css("tbody tr").click()
        # clicks check out 
        self.driver.find_css('.btn-checkin').click()
        # at the checkin page
        self.driver.click_submit()
        device = Device.objects.get(pk=self.device.pk)
        assert_equal(device.status, Device.CHECKED_IN)
        assert_in('Successfully checked in', self.driver.body_text())

    def test_can_checkout_device_to_subject(self):
        # clicks on the table row for the device
        self.driver.find_css('tbody tr').click()
        # clicks check out
        self.driver.find_css('.btn-checkout').click()
        dialog = self.driver.switch_to_alert()
        dialog.send_keys()
