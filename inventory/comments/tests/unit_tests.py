'''Unit tests for the comments models.'''
from nose.tools import *
from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse

from inventory.comments.tests.factories import (IpadCommentFactory,
        HeadphonesCommentFactory, create_comment_factories)


class IpadCommentTest(TestCase):
    def setUp(self):
        self.comment = IpadCommentFactory()

    def test_updated_at(self):
        then = timezone.now()
        # Upon saving, updated_at field is updated
        self.comment.save()
        assert_true(self.comment.updated_at > then)

    def test_get_cname(self):
        assert_equal(self.comment.get_cname(), 'comment')

    def test_device_updated_at(self):
        then = timezone.now()
        self.comment.save()
        assert_true(self.comment.device.updated_at > then)


class HeadphonesCommentTest(TestCase):
    def setUp(self):
        self.comment = HeadphonesCommentFactory()

    def test_updated_at(self):
        then = timezone.now()
        # Upon saving, updated_at field is updated
        self.comment.save()
        assert_true(self.comment.updated_at > then)

    def test_device_updated_at(self):
        then = timezone.now()
        self.comment.save()
        assert_true(self.comment.device.updated_at > then)


class CommentPropertiesTest(TestCase):
    """Test the properties for all comment models."""
    def setUp(self):
        self.comments = create_comment_factories()

    def test_edit_urls(self):
        ipad_edit_url = reverse('comments:ipad_edit', args=(
                            self.comments[0].device.pk,
                            self.comments[0].pk))

        headphones_edit_url = reverse('comments:headphones_edit', args=(
                            self.comments[1].device.pk,
                            self.comments[1].pk))

        adapter_edit_url = reverse('comments:adapter_edit', args=(
                            self.comments[2].device.pk,
                            self.comments[2].pk))

        case_edit_url = reverse('comments:case_edit', args=(
                            self.comments[3].device.pk,
                            self.comments[3].pk))

        urls = (ipad_edit_url, headphones_edit_url, 
                adapter_edit_url, case_edit_url)

        for comment, edit_url in zip(self.comments, urls):
            assert_equal(comment.edit_url, edit_url)

    def test_device_urls(self):
        ipad_url = reverse('devices:ipad_detail', args=(
                            self.comments[0].device.pk,))

        headphones_url = reverse('devices:headphones_detail', args=(
                            self.comments[1].device.pk,))

        adapter_url = reverse('devices:adapter_detail', args=(
                            self.comments[2].device.pk,))

        case_url = reverse('devices:case_detail', args=(
                            self.comments[3].device.pk,))

        urls = (ipad_url, headphones_url, adapter_url, case_url)

        for comment, detail_url in zip(self.comments, urls):
            assert_equal(comment.device_url, detail_url)

