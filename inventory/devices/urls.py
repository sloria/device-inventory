"""urlconf for the base application"""

from django.conf.urls.defaults import url, patterns
from django.views.generic import TemplateView
from inventory.devices.views import *


urlpatterns = patterns('',
    # ex: /devices
    url(r'^$', 
        DevicesListView.as_view(),
        kwargs={'device_type': 'ipads'},
        name='index'),

    # ex: /devices/ipads/
    url(r'^ipads/$', 
        DevicesListView.as_view(),
        kwargs={'device_type': 'ipads'},
        name='ipads'),

    # ex: /devices/headphones/
    url(r'^headphones/$', 
        DevicesListView.as_view(),
        kwargs={'device_type': 'headphones'},
        name='headphones'),

    # ex: /devices/adapters/
    url(r'^adapters/$', 
        DevicesListView.as_view(),
        kwargs={'device_type': 'adapters'},
        name='adapters'),

    # ex: /devices/cases/
    url(r'^cases/$', 
        DevicesListView.as_view(),
        kwargs={'device_type': 'cases'},
        name='cases'),

    # ex: /devices/ipads/3/
    url(r'^ipads/(?P<pk>\d+)/$',
        IpadDetail.as_view(),
        name='ipad_detail'),

    # ex: /devices/headphones/3/
    url(r'^headphones/(?P<pk>\d+)/$',
        HeadphonesDetail.as_view(),
        name='ipad_detail'),

    # ex: /devices/adapters/3/
    url(r'^adapters/(?P<pk>\d+)/$',
        AdapterDetail.as_view(),
        name='adapter_detail'),

    # ex: /devices/cases/3/
    url(r'^cases/(?P<pk>\d+)/$',
        CaseDetail.as_view(),
        name='case_detail'),

    # ex: /devices/add
    url(r'^add/$', 
        DeviceAdd.as_view(),
        name='add'),

    url(r'^permissions/denied/$',
        TemplateView.as_view(template_name='403.html'),
        name='permission_denied'),
    
    # ex: /devices/3/delete/
    url(r'^(?P<pk>\d+)/delete/$',
        DeviceDelete.as_view(),
        name='delete'),

    # ex: /devices/ipads/3/checkout
    url(r'^(?P<device_type>\w+)/(?P<pk>\d+)/checkout/$',
        DeviceCheckout.as_view(),
        name='device_checkout'),

    # ex: /devices/ipads/3/checkout/confirm
    url(r'^(?P<device_type>\w+)/(?P<pk>\d+)/checkout/confirm/$',
        DeviceCheckoutConfirm.as_view(),
        name='checkout_confirm'),

    # ex: /devices/ipads/3/checkin
    url(r'^(?P<device_type>\w+)/(?P<pk>\d+)/checkin/$',
        DeviceCheckin.as_view(),
        name='checkin'),

    # ex: /devices/ipads/3/edit
    url(r'^ipads/(?P<pk>\d+)/edit/$',
        IpadUpdate.as_view(),
        name='ipad_update'),

    # ex: /devices/headphones/3/edit
    url(r'^headphones/(?P<pk>\d+)/edit/$',
        HeadphonesUpdate.as_view(),
        name='headphones_update'),

    # ex: /devices/cases/3/edit
    url(r'^cases/(?P<pk>\d+)/edit/$',
        CaseUpdate.as_view(),
        name='case_update'),

    # ex: /devices/adapters/3/edit
    url(r'^adapters/(?P<pk>\d+)/edit/$',
        AdapterUpdate.as_view(),
        name='adapter_update'),

    # ex: /devices/3/comment/4/delete
    url(r'^(?P<device_id>\d+)/comment/(?P<comment_id>\d+)/delete/$',
        CommentDelete.as_view(),
        name='delete_comment'),

        # ex: /devices/3/comment/4/edit
    url(r'^(?P<device_id>\d+)/comment/(?P<comment_id>\d+)/edit/$',
        CommentEdit.as_view(),
        name='edit_comment'),


)
