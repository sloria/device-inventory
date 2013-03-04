"""urlconf for the base application"""

from django.conf.urls.defaults import url, patterns
from inventory.devices.views import *

urlpatterns = patterns('',
    url(r'^$', 
        DevicesListView.as_view(),
        name='index'),
)
