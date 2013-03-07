# Create your views here.
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import ListView, CreateView, DeleteView

from inventory.devices.models import Device
from inventory.devices.forms import DeviceForm

class DevicesListView(ListView):
    '''Index view for devices.'''
    model = Device
    template_name = 'devices/index.html'
    context_object_name = 'all_devices'

    def get(self, request):
        '''Get request takes user to index view if authenticated.
        Otherwise, redirect back to the home page.'''
        if request.user.is_authenticated():
            return super(DevicesListView, self).get(self, request)
        else:
            return redirect('home')

    def post(self, request):
        """Process the action for the selected devices.
        """
        action = request.POST['action']  # the selected action
        selected_pks = [int(v) for v in request.POST.getlist('device_select')]
        # Get the selected Device objects
        selected_devices = Device.objects.filter(pk__in=selected_pks)

        if action == 'delete_selected': 
            selected_devices.delete() # delete selected
            messages.success(request, 
                    'Successfully deleted {} devices'.format(len(selected_pks)))
        return redirect('devices:index')

class DeviceAdd(CreateView):
    '''View for adding a device.
    '''
    form_class = DeviceForm
    template_name = 'devices/add.html'
    success_url = reverse_lazy('devices:index')

    def get(self, request):
        '''Get request renders form if user has permission to add
        a device. Otherwise, redirects to 403 page.'''
        if request.user.has_perms('devices.add_device'):
            return super(DeviceAdd, self).get(self, request)
        else:
            return redirect('devices:permission_denied')

class DeviceDelete(DeleteView):
    ''' View for deleting a single instance.
    '''
    model = Device
    template_name = 'devices/delete.html'
    context_object_name = 'object'

    def get_success_url(self):
        return reverse_lazy('devices:index')


