'''Functional tests using WebTest'''

from django_webtest import WebTest
from nose.tools import *
from inventory.user.tests.factories import UserFactory
from inventory.devices.tests.factories import *

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

    def test_redirected_to_login_if_not_logged_in(self):
        res = self.app.get('/devices/')
        res = res.follow()
        assert_equal(res.status_code, 200)
        assert_equal(res.request.path, '/')

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

class TestAnExperimenter(WebTest):
    def setUp(self):
        self.experimenter = ExperimenterFactory()

    def test_cannot_create_device(self):
        # goes to root (logged in)
        res = self.app.get('/', user=self.experimenter.user).follow()
        assert_equal(res.request.path, '/devices/')
        assert_not_in('Add device', res)
        # tries to go directly to the add device page
        res = self.app.get('/devices/add/', user=self.experimenter.user).follow()
        # sees a not authorized warning
        assert_in('Forbidden', res)

class TestASuperUser(WebTest):
    def setUp(self):
        self.admin = UserFactory()
        self.admin.is_superuser = True
        self.admin.save()

    def tearDown(self):
        pass

    def test_can_create_device(self):
        # Goes to root (already logged in)
        res = self.app.get('/', user=self.admin).follow()
        assert_equal(res.request.path, '/devices/')
        # There's an Add device button
        assert_in('Add device', res)
        res = res.click('Add device')
        assert_equal(res.request.path, '/devices/add/')


class TestAReader(WebTest):
    def setUp(self):
        self.reader = ReaderFactory()

    def test_cannot_create_device(self):
        # goes to root (logged in)
        res = self.app.get('/', user=self.reader.user).follow()
        # at the devices page
        assert_equal(res.request.path, '/devices/')
        # there's no Add device button
        assert_not_in('Add device', res)

        # tries to go directly to the add device page
        res = self.app.get('/devices/add/', user=self.reader.user).follow()
        # sees a not authorized warning
        # res.showbrowser()
        assert_in('Forbidden', res)



