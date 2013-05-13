"""Devices views."""
import re
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import simplejson as json
from django.views.generic import (View, DetailView, TemplateView,
                                    UpdateView, FormView)
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
import verhoeff

from inventory.devices.models import *
from inventory.user.models import Subject, Lendee
from inventory.devices.forms import (DeviceForm, CheckinForm, 
    CommentEditForm, IpadUpdateForm, AdapterUpdateForm,
    CaseUpdateForm, HeadphonesUpdateForm)

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

class DevicesListView(TemplateView):
    '''Index view for devices. This serves as a list view 
    for all device types.'''
    template_name = 'devices/index.html'

    def get(self, request, **kwargs):
        if request.user.is_authenticated():
            return super(DevicesListView, self).get(request)
        else:
            return redirect('home')

    def get_context_data(self, **kwargs):
        device_type = self.kwargs['device_type']
        device_class = None
        if device_type == 'ipads':
            device_class = Ipad
        elif device_type == 'headphones':
            device_class = Headphones
        elif device_type == 'adapters':
            device_class = Adapter
        elif device_type == 'cases':
            device_class = Case

        context = super(DevicesListView, self).get_context_data(**kwargs)
        context['contenttype_id'] = ContentType.objects\
                                        .get_for_model(device_class).pk
        context['all_devices'] = device_class.objects.all()
        context['device_type'] = self.kwargs['device_type'].capitalize()
        return context

class IpadDetail(DetailView):
    """Detail view for iPads.
    """
    model = Ipad
    context_object_name = 'device'
    template_name = 'devices/detail.html'

class DeviceAdd(FormView):
    '''View for adding a device.
    '''
    form_class = DeviceForm
    template_name = 'devices/add.html'
    success_url = reverse_lazy('devices:index')

    def _add_device_type(self, device_class, form):
        '''Saves a new device record of a given class (e.g. Ipad)
        with the attributes submitted in a form.
        '''
        form_data = form.cleaned_data
        device = device_class()
        if form_data['description']:
            device.description = form_data['description']
        if form_data['responsible_party']:
            device.responsible_party = form_data['responsible_party']
        device.make = form_data['make']
        if form_data['serial_number']:
            device.serial_number = form_data['serial_number']
        device.purchased_at = form_data['purchased_at']
        device.save()


    def form_valid(self, form):
        """Create a new device of the selected type.
        """
        form_data = form.cleaned_data
        device_type = form_data['device_type']
        if device_type == 'ipad':
            self._add_device_type(Ipad, form)
        elif device_type == 'headphones':
            self._add_device_type(Headphones, form)
        elif device_type == 'adapter':
            self._add_device_type(Adapter, form)
        else:
            self._add_device_type(Case, form)
        return super(DeviceAdd, self).form_valid(form)

    def get(self, request):
        '''Get request renders form if user has permission to add
        a device. Otherwise, redirects to 403 page.'''
        if request.user.has_perms('devices.add_device'):
            return super(DeviceAdd, self).get(self, request)
        else:
            return redirect('devices:permission_denied')

class DeviceDelete(View):
    def post(self, request, pk):
        """Deletes the device with the given pk.
        """
        data = {}
        Device.objects.filter(pk=pk).delete()
        messages.success(request, 'Successfully deleted device.')
        data['success'] = True
        json_data = json.dumps(data)
        return HttpResponse(json_data, mimetype="application/json")

class CommentEdit(UpdateView):
    template_name = "devices/edit_comment.html"
    model = Comment
    form_class = CommentEditForm
    pk_url_kwarg = "comment_id"

    def form_valid(self, form):
        # Update the devices updated_at attribute before saving
        Ipad.objects.filter(pk=int(self.kwargs['device_id']))\
                                .update(updated_at=timezone.now())
        return super(CommentEdit, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('devices:detail', args=[self.kwargs['device_id']])

class CommentDelete(View):
    def post(self, request, device_id, comment_id):
        '''Deletes the comment with the given pk.
        '''
        data = {}
        Comment.objects.filter(pk=comment_id).delete()
        messages.success(request, 'Successfully deleted comment.')
        data['success'] = True
        data['pk'] = comment_id
        json_data = json.dumps(data)
        return HttpResponse(json_data, mimetype='application/json')

class DeviceCheckout(View):
    '''View for checking out a device.
    Passes a list of possible lendees to the template for selection.
    '''
    def post(self, request, pk):
        '''Checks out a device to either a user or a subject.
        '''
        # get the post data (a string that's either a subject ID or e-mail address)
        lendee_str = request.POST['lendee']
        response_data = {}

        # If it's an email (a user)
        if EMAIL_REGEX.match(lendee_str):
            try:
                # get the user
                user = User.objects.get(username=lendee_str)
                # get or create the lendee with the user as the user
                response_data['name'] = user.get_full_name()
                Lendee.objects.get_or_create(user=user)
                response_data['success'] = True
            except ObjectDoesNotExist:
                response_data['error'] = 'No user found with e-mail address {email}'\
                                                    .format(email=lendee_str)
        # Else it's a subject id
        else:
            # remove dashes and cast as int
            subject_id = int(lendee_str.replace('-', '')) 
            # validate the id using the Verhoeff algorithm
            if verhoeff.validate(subject_id):
                # get or create the subject
                subject, created = Subject.objects.get_or_create(
                                                    subject_id=subject_id)
                if created:
                    response_data['created_subject'] = True
                else:
                    response_data['created_subject'] = False
                # get or create the lendee with the subject as the lendee
                lendee_obj, created = Lendee.objects.get_or_create(
                                                        subject=subject)
                response_data['name'] = "Subject {id}".format(id=subject_id)
                response_data['success'] = True
            else:
                response_data['error'] = "Invalid subject ID. Please try again."

        # return json response
        json_data = json.dumps(response_data)
        return HttpResponse(json_data, mimetype='application/json')

class DeviceCheckoutConfirm(View):
    '''View for confirming the checkout of a device.
    Accepts and AJAX request and updates a device record.
    '''
    def _checkout_device(self, pk, lendee, lender):
        '''Checks out the selected device.
        '''
        # Get the correct device type from POST data
        device_type = self.request.POST['device_type']
        device_class = None
        if device_type == 'ipad':
            device_class = Ipad
        elif device_type == 'headphones':
            device_class = Headphones
        elif device_type == 'adapter':
            device_class = Adapter
        else:
            device_class = Case
        # Initialize the new device object
        device = device_class.objects.get(pk=pk)
        device.lendee = lendee
        device.lender = lender
        device.status = Device.CHECKED_OUT
        device.save()
        return device

    def post(self, request, pk):
        response_data = {}
        # Lendee email has already been validated in DeviceCheckout
        lendee_str = request.POST['lendee']
        # If lendee is a user
        if EMAIL_REGEX.match(lendee_str):
            lendee_obj = Lendee.objects.get(user__username=lendee_str)
        # if lendee is a subject
        else:
            # remove dashes and cast as int
            subject_id = int(lendee_str.replace('-', ''))
            lendee_obj = Lendee.objects.get(subject__subject_id=subject_id)
        # Update the device's lendee, lender, status, and updated at time
        self._checkout_device(pk, lendee_obj, request.user)
        response_data['success'] = True
        json_data = json.dumps(response_data)
        messages.success(request, 'Successfully checked out device')
        return HttpResponse(json_data, mimetype='application/json')


class DeviceCheckin(FormView):
    form_class = CheckinForm
    template_name = 'devices/checkin.html'
    success_url = reverse_lazy('devices:index')

    def _get_device(self, pk):
        '''Gets the device of the correct type and pk from the POST data.
        Returns the device object.
        '''
        # get the correct device type from POST data
        device_type = self.kwargs['device_type']
        device_class = None
        if device_type == 'ipad':
            device_class = Ipad
        elif device_type == 'headphones':
            device_class = Headphones
        elif device_type == 'adapter':
            device_class = Adapter
        else:
            device_class = Case
        # Initialize the new device object
        device = device_class.objects.get(pk=pk)
        return device

    def form_valid(self, form):
        # Get the device
        device = self._get_device(self.kwargs['pk'])
        # Change device status
        if form.cleaned_data['condition'] == 'broken':
            device.status = Device.BROKEN
            device.condition = Device.BROKEN
        elif form.cleaned_data['condition'] == 'scratched':
            device.status = Device.CHECKED_IN_NOT_READY
            device.condition = Device.SCRATCHED
        elif form.cleaned_data['condition'] == 'missing':
            device.status = Device.MISSING
            device.condition = Device.MISSING
        else:
            device.status = Device.CHECKED_IN_NOT_READY
            device.condition = Device.EXCELLENT

        # Set the lendee and lender to None
        device.lendee = None
        device.lender = None
        device.save()
        # save the comment if it exists
        if form.cleaned_data['comment']:
            Comment.objects.create(text=form.cleaned_data['comment'],
                                    device=device,
                                    user = self.request.user)
        messages.success(self.request, 'Successfully checked in')
        # Change device condition
        return super(DeviceCheckin, self).form_valid(form)

class DeviceUpdateView(UpdateView):
    template_name = 'devices/edit.html'
    context_object_name = 'device'

class IpadUpdate(DeviceUpdateView):
    model = Ipad
    form_class = IpadUpdateForm
    success_url = reverse_lazy('devices:ipads')

class HeadphonesUpdate(DeviceUpdateView):
    model = Headphones
    form_class = HeadphonesUpdateForm
    success_url = reverse_lazy('devices:headphones')

class AdapterUpdate(DeviceUpdateView):
    model = Adapter
    form_class = AdapterUpdateForm
    success_url = reverse_lazy('devices:adapters')

class CaseUpdate(DeviceUpdateView):
    model = Case
    form_class = CaseUpdateForm
    success_url = reverse_lazy('devices:cases') 
