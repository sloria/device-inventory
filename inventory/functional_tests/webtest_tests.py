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
        assert_in('Inventory', res)


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

    def test_can_see_devices(self):
        pass


