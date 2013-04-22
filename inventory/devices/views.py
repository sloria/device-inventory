# Create your views here.
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import simplejson as json
from django.views.generic import View, ListView, CreateView, DeleteView, UpdateView, FormView
import verhoeff

from inventory.devices.models import Device, Lendee
from inventory.user.models import Subject
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
    # TODO
    def get(self, request, pk):
        request.session['last_device_id'] = pk
        if Lendee.objects.exists():
            lendees = Lendee.objects.all()
            return render(request, 'devices/checkout.html', {'lendees': lendees})
        else:
            return render(request, 'devices/checkout.html', {'lendees': False})

    def post(self, request, pk):
        '''Checks out a device to either a user or a subject.
        '''
        # get the lendee id (a string that's either a subject ID or
        # an user's name (or maybe email address?)
        lendee = request.POST['lendee']
        data = {}
        try:
            # if it's a valid subject id
            subject_id = int(lendee)
            if verhoeff.validate(subject_id):
                # get or create the subject
                subject, created = Subject.objects.get_or_create(subject_id=subject_id)
                if created:
                    data['created_subject'] = True
                else:
                    data['created_subject'] = False
                # get or create the lendee with the subject as the lendee
                lendee_obj, created = Lendee.objects.get_or_create(subject=subject)
                data['name'] = "Subject {id}".format(id=subject_id)
                data['success'] = True
            else:
                data['error'] = "Invalid subject ID. Please try again."
        # else it's a user
        except ValueError:
            try:
                # get the user
                user = User.objects.get(username=lendee)
                # get or create the lendee with the user as the user
                data['name'] = user.get_full_name()
                Lendee.objects.get_or_create(user=user)
                data['success'] = True
            except ObjectDoesNotExist:
                data['error'] = 'No user found with e-mail address {email}'.format(email=lendee)
            # return json response
        json_data = json.dumps(data)
        return HttpResponse(json_data, mimetype='application/json')

        # return redirect('devices:index')

class DeviceCheckoutConfirm(View):
    '''View for confirming the checkout of a device.
    Accepts and AJAX request and updates a device record.
    '''
    def post(self, request, pk):
        data = {}
        # Lendee email has already been validate in DeviceCheckout
        lendee = request.POST['lendee']
        try:
            # if lendee is a subject
            subject_id = int(lendee)
            lendee_obj = Lendee.objects.get(subject__subject_id=subject_id)
        except ValueError:
            # if lendee is a user
            lendee_obj = Lendee.objects.get(user__username=lendee)
        # Update the device's lendee, lender, and status
        Device.objects.filter(pk=pk).update(lendee=lendee_obj,
                                            lender=request.user,
                                            status=Device.CHECKED_OUT)
        data['success'] = True
        json_data = json.dumps(data)
        messages.success(request, 'Successfully checked out device')
        return HttpResponse(json_data, mimetype='application/json')


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
        # Set the lendee and lender to None
        device.lendee = None
        device.lender = None
        device.save()
        messages.success(self.request, 'Successfully checked in')
        # Change device condition
        return super(DeviceCheckin, self).form_valid(form)

class DeviceUpdate(UpdateView):
    model = Device


