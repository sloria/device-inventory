"""Devices views."""

import re
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import simplejson as json
from django.views.generic import (View, ListView, DetailView,
    CreateView, UpdateView, FormView)
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
import verhoeff

from inventory.devices.models import Device, Comment
from inventory.user.models import Subject, Lendee
from inventory.devices.forms import DeviceForm, CheckinForm, CommentEditForm

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

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

    def get_context_data(self, **kwargs):
        context = super(DevicesListView, self).get_context_data(**kwargs)
        context['contenttype_id'] = ContentType.objects.get_for_model(Device).pk
        return context

class DeviceDetail(DetailView):
    """Detail view for devices.
    """
    model = Device
    context_object_name = 'device'
    template_name = 'devices/detail.html'


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
        Device.objects.filter(pk=int(self.kwargs['device_id']))\
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
        device = Device.objects.get(pk=pk)
        device.lendee = lendee_obj
        device.lender = request.user
        device.status = Device.CHECKED_OUT
        device.updated_at = timezone.now()
        device.save()
        response_data['success'] = True
        json_data = json.dumps(response_data)
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
        device.updated_at = timezone.now()
        device.save()
        # save the comment if it exists
        if form.cleaned_data['comment']:
            Comment.objects.create(text=form.cleaned_data['comment'],
                                    device=device,
                                    user = self.request.user)
        messages.success(self.request, 'Successfully checked in')
        # Change device condition
        return super(DeviceCheckin, self).form_valid(form)

class DeviceUpdate(UpdateView):
    model = Device
    template_name = 'devices/edit.html'
    context_object_name = 'device'

    def get_success_url(self):
        return reverse_lazy('devices:index')
