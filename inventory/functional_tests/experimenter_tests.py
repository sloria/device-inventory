'''Functional tests for an Experimenter User'''

from django_webtest import WebTest
from nose.tools import *
from inventory.user.tests.factories import UserFactory, ExperimenterFactory
from inventory.devices.tests.factories import IpadFactory
from inventory.devices.models import Comment

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
        IpadFactory()
        # goes to devices page
        res = self.app.get('/', user=self.experimenter.user).follow()
        # cannot see delete device
        assert_not_in('Delete', res)

    def test_can_see_devices(self):
        # a device is already created
        device = IpadFactory()
        # goes to the device index
        res = self.app.get('/', user=self.experimenter.user).follow()
        # sees the device name
        res.mustcontain(device.name, 
                        device.get_status_display(), 
                        device.get_condition_display(),
                        device.serial_number)

    def test_cannot_create_users(self):
        # logs in 
        res = self.app.get('/', user=self.experimenter.user).follow()
        assert_not_in('Create user', res)

    def test_can_see_device_detail(self):
        # a device is created
        device = IpadFactory()
        # goes to its detail page
        res = self.app.get('/devices/{pk}/'.format(pk=device.pk))
        res.mustcontain(device.name,
                        device.get_verbose_status(),
                        device.get_condition_display(),
                        device.serial_number)
        assert_in('Check-in Comments', res)

    def test_can_edit_comment(self):
        # A device is created
        device = IpadFactory()
        # It has a check-in comment
        comment = Comment.objects.create(text="Just a bigger iPhone", 
                                        device=device,
                                        user=self.experimenter.user)
        # goes to the detail page
        res = self.app.get('/devices/{pk}/'.format(pk=device.pk), 
                                            user=self.experimenter.user)
        # can see the comment
        assert_in(comment.text, res)
        # clicks the edit link
        res = res.click('Edit')
        # sees a form
        assert_in('Edit comment', res)
        form = res.forms['id-edit_comment_form']
        # changes the comment text
        form['text'] = 'Or a flat MacBook Air'
        # submits the form
        res = form.submit().follow()
        # back at the detail page
        assert_equal(res.request.path, '/devices/{pk}/'.format(pk=device.pk))
        # sees the new comment text
        assert_in('Or a flat MacBook Air', res)
