'''Functional tests using Selenium'''

from inventory.user.tests.factories import ExperimenterFactory
from inventory.devices.tests.factories import DeviceFactory

from inventory.selenium_tests.utils import SeleniumTestCase, CustomWebDriver

class TestAnExperimenter(SeleniumTestCase):

    def setUp(self):
        # Create a user (Experimenter)
        ExperimenterFactory()
        self.driver = CustomWebDriver()

    def test_can_login(self):
        self.open('/')


    def tearDown(self):
        self.driver.quit()

