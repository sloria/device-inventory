'''Provides a base test class and helper methods for
Selenium testing.
'''
from django.test import LiveServerTestCase
from django.conf import settings
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

# Determine the WebDriver module. default to Firefox
try:
    web_driver_module = settings.SELENIUM_WEBDRIVER
except AttributeError:
    from selenium.webdriver.firefox import webdriver as web_driver_module

class SeleniumTestCase(LiveServerTestCase):
    """A base test case for Selenium, providing helper methods
    for generating clients and logging in profiles.
    """

    def open(self, url):
        self.driver.get("{root}{url}".format(
                        root=self.live_server_url, url=url))

class CustomWebDriver(web_driver_module.WebDriver):
    """Custom WebDriver with some helpers added.
    """

    def find_css(self, css_selector):
        '''Shortcut to find elements by CSS. Returns either
        a list or singleton.
        '''
        elems = self.find_elements_by_css_selector(css_selector)
        found = len(elems)
        if found == 1:
            return elems[0]
        elif not elems:
            raise NoSuchElementException(css_selector)
        return elems

    def wait_for_css(self, css_selector, timeout=7):
        """Shortcut for WebDriverWait
        """
        try:
            return WebDriverWait(self, timeout).\
                    until(lambda driver: driver.find_css(css_selector))
        except:
            self.quit()

    def body_text(self):
        '''Shortcut for accessing the text within the <body> of the DOM.
        
        Example:
        >> assert_in('Some text', self.driver.body_text())
        '''
        return self.find_element_by_tag_name('body').text

    def click_submit(self):
        '''Shortcut for clicking the submit button on a webpage.
        '''
        return self.find_css("input[type='submit']").click()
