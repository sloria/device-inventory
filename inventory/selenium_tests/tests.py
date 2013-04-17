'''Functional tests using Selenium'''
from nose.tools import *
import time
from inventory.user.tests.factories import ExperimenterFactory
from inventory.devices.tests.factories import DeviceFactory

from inventory.selenium_tests.utils import SeleniumTestCase, CustomWebDriver

class TestAnExperimenter(SeleniumTestCase):

    def setUp(self):
        # Create a user (Experimenter)
        self.experimenter = ExperimenterFactory()
        # create a device
        DeviceFactory()
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

    def test_can_checkout_device(self):
        # at the device index page
        assert_in('Devices', self.driver.body_text())
        assert_not_in('12345', self.driver.body_text())
        # clicks on the table row for the device
        self.driver.find_css('tbody tr').click()
        # clicks check out
        self.driver.find_css('.btn-checkout').click()
        # a javascript input dialog pops up
        dialog = self.driver.switch_to_alert()
        print dialog.text
        # types in subject id
        dialog.send_keys('12345')
        # click accept
        dialog.accept()
        assert_in('12345', self.driver.body_text())
        assert False, 'finish me'
