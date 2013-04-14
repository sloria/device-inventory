"""urlconf for the base application"""

from django.conf.urls.defaults import url, patterns
from django.views.generic import TemplateView
from inventory.devices.views import *


urlpatterns = patterns('',
    url(r'^$', 
        DevicesListView.as_view(),
        name='index'),

    url(r'^add/$', 
        DeviceAdd.as_view(),
        name='add'),

    url(r'^permissions/denied/$',
        TemplateView.as_view(template_name='403.html'),
        name='permission_denied'
        ),
    
    # ex: /devices/3/delete/
    url(r'^(?P<pk>\d+)/delete/$',
        DeviceDelete.as_view(),
        name='delete'
        ),

    # ex: /devices/3/checkout
    url(r'^(?P<pk>\d+)/checkout/$',
        DeviceCheckout.as_view(),
        name='checkout'),

    # ex: /devices/3/checkin
    url(r'^(?P<pk>\d+)/checkin/$',
        DeviceCheckin.as_view(),
        name='checkin'),

    url(r'^(?P<pk>\d+)/edit/$',
        DeviceUpdate.as_view(),
        name='update')
)
