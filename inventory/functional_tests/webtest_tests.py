'''Functional tests using WebTest'''

from django_webtest import WebTest
from nose.tools import *
from inventory.user.tests.factories import UserFactory

class TestAUser(WebTest):

    def setUp(self):
        self.user = UserFactory()

    def tearDown(self):
        pass

    def test_can_see_homepage(self):
        # Rosie goes to homepage
        res = self.app.get('/')
        assert_equal(res.status_code, 200)

    def test_can_login(self):
        # Rosie goes to homepage
        res = self.app.get('/')
        # Rosie logs in
        form = res.forms['loginForm']
        form['username'] = self.user.username
        form['password'] = self.user.password
        res = form.submit()
        assert_equal(res.status_code, 200)
        assert_true(self.user.is_authenticated())

    def test_can_signup(self):
        # Rosie goes to homepage
        res = self.app.get('/')
        # She clicks sign up 
        res = res.click('Register')
        assert_equal(res.status_code, 200)
        
