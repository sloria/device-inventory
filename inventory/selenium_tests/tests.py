'''Functional tests using Selenium'''
from nose.tools import *
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
        # types in user's email address
        dialog.send_keys(self.experimenter.user.username)
        # click accept
        dialog.accept()
        # a dialog appears
        dialog = self.driver.switch_to_alert()
        # it shows the lendee's name
        assert_in('Confirm check out to {name}?'.\
                format(name=self.experimenter.user.get_full_name()),
                dialog.text)
        assert False, 'finish me'

    def test_can_checkout_device_to_subject(self):
        assert False, 'finish me'
