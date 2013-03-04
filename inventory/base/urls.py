"""urlconf for the base application"""

from django.conf.urls.defaults import url, patterns

import django.contrib.auth.views as auth_views
from inventory.base.views import home


urlpatterns = patterns('inventory.base.views',
    url(r'^$', 
        'home',
        name='home'),
)
