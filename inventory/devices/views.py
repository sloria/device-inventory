# Create your views here.
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import View, ListView, CreateView, DeleteView, FormView

from inventory.devices.models import Device, Lendee
from inventory.devices.forms import DeviceForm, CheckinForm

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
            selected_devices.delete() # delete selected from database
            messages.success(request, 
                    'Successfully deleted {} devices'.format(len(selected_pks)))
        elif action in ('checkout_selected', 'checkin_selected'):
            # Make sure user selected one and only one device 
            if len(selected_devices) > 1:
                message = ''
                if action == 'checkout_selected':
                    message = 'Cannot check out more than one device at a time'
                elif action == 'checkin_selected':
                    message = 'Cannot check in more than one device at a time'
                messages.error(request, message)
            elif len(selected_devices) == 0:
                messages.error(request, 'No devices selected.')
            else:
                # redirect to lendee selection page
                device = selected_devices[0]
                if action == 'checkout_selected':
                    return redirect('devices:checkout',pk=device.pk)
                elif action == 'checkin_selected':
                    return redirect('devices:checkin', pk=device.pk)
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

class DeviceCheckout(View):
    '''View for checking out a device.
    Passes a list of possible lendees to the template for selection.
    '''

    def get(self, request, pk):
        if Lendee.objects.exists():
            lendees = Lendee.objects.all()
            return render(request, 'devices/checkout.html', {'lendees': lendees})
        else:
            return render(request, 'devices/checkout.html', {'lendees': False})

    def post(self, request, pk):
        # Get the device
        device = Device.objects.get(pk=pk)
        # Get the pk of the selected lendee
        selected_lendee_pk = int(request.POST.get('lendee_select'))
        # Get the ledee object
        lendee = Lendee.objects.get(pk=selected_lendee_pk)
        # Update the device's lendee and lender attributes
        device.lendee = lendee
        device.lender = request.user
        device.save()
        return redirect('devices:index')

class DeviceCheckin(FormView):
    form_class = CheckinForm
    template_name = 'devices/checkin.html'
    success_url = reverse_lazy('devices:index')

    def form_valid(self, form):
        # Get the device
        device = Device.objects.get(pk=self.kwargs['pk'])
        # Change device status
        if form.cleaned_data['condition'] == 'broken':
            device.status = Device.BROKEN
            device.condition = Device.BROKEN
        elif form.cleaned_data['condition'] == 'scratched':
            device.status = Device.CHECKED_IN
            device.condition = Device.SCRATCHED
        elif form.cleaned_data['condition'] == 'missing':
            device.status = Device.MISSING
            device.condition = Device.MISSING
        else:
            device.status = Device.CHECKED_IN
            device.condition = Device.EXCELLENT
        # Set the lendee and lenderto None
        device.lendee = None
        device.lender = None
        device.save()
        messages.success(self.request, 'Successfully checked in')
        # Change device condition
        return super(DeviceCheckin, self).form_valid(form)

