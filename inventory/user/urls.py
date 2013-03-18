"""urlconf for the base application"""

from django.conf.urls.defaults import url, patterns
from django.views.generic import TemplateView
from inventory.user.views import UserAdd


urlpatterns = patterns('',

    # ex: /users/add
    url(r'^add/$', 
        UserAdd.as_view(),
        name='add'),
)
