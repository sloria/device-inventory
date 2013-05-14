"""urlconf for devices"""

from django.conf.urls.defaults import url, patterns
from inventory.comments.views import *

urlpatterns = patterns('',
    # ex: /devices/comments/12/ipads/3/delete/
    url(r'^(?P<comment_id>\d+)/ipads/(?P<device_id>\d+)/delete/$',
        IpadCommentDelete.as_view(),
        name='ipad_delete'),

    # ex: /devices/comments/12/ipads/3/edit/
    url(r'^(?P<comment_id>\d+)/ipads/(?P<device_id>\d+)/edit/$',
        IpadCommentUpdate.as_view(),
        name='ipad_edit'),

    # ex: /devices/comments/12/headphones/3/delete/
    url(r'^(?P<comment_id>\d+)/headphones/(?P<device_id>\d+)/delete/$',
        HeadphonesCommentDelete.as_view(),
        name='headphones_delete'),

    # ex: /devices/comments/12/headphones/3/edit/
    url(r'^(?P<comment_id>\d+)/headphones/(?P<device_id>\d+)/edit/$',
        HeadphonesCommentUpdate.as_view(),
        name='headphones_edit'),

    # ex: /devices/comments/12/adapters/3/delete/
    url(r'^(?P<comment_id>\d+)/adapters/(?P<device_id>\d+)/delete/$',
        AdapterCommentDelete.as_view(),
        name='adapter_delete'),

    # ex: /devices/comments/12/adapters/3/edit/
    url(r'^(?P<comment_id>\d+)/adapters/(?P<device_id>\d+)/edit/$',
        AdapterCommentUpdate.as_view(),
        name='adapter_edit'),

    # ex: /devices/comments/12/cases/3/delete/
    url(r'^(?P<comment_id>\d+)/cases/(?P<device_id>\d+)/delete/$',
        CaseCommentDelete.as_view(),
        name='case_delete'),

    # ex: /devices/comments/12/cases/3/edit/
    url(r'^(?P<comment_id>\d+)/cases/(?P<device_id>\d+)/edit/$',
        CaseCommentUpdate.as_view(),
        name='case_edit'),
)