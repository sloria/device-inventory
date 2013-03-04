# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.generic import ListView

from inventory.devices.models import Device

class LoggedInMixin(object):
    """ A mixin requiring a user to be logged in. """
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            raise Http404
        return super(LoggedInMixin, self).dispatch(request, *args, **kwargs)

class DevicesListView(LoggedInMixin, ListView):
    model = Device
    template_name = 'devices/index.html'
    context_object_name = 'all_devices'
