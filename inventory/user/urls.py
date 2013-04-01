"""urlconf for the base application"""

from django.conf.urls.defaults import url, patterns
from django.views.generic import TemplateView
from inventory.user.views import CreateUser, CreateSubject


urlpatterns = patterns('',

    # ex: /users/add
    url(r'^add/$', 
        CreateUser.as_view(),
        name='create_user'),

    # ex: /users/subject/add
    url(r'^subject/add/$', 
        CreateSubject.as_view(), 
        name='create_subject')
)
