# Create your views here.
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import FormView, CreateView

from inventory.user.models import Subject, Lendee
from inventory.user.forms import UserForm, SubjectForm

class CreateUser(FormView):
    '''View for adding a user.
    '''
    form_class = UserForm
    template_name = 'user/create_user.html'
    success_url = reverse_lazy('devices:index')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 
            'Successfully created user: {0}'.format(form.cleaned_data['email']))
        return super(CreateUser, self).form_valid(form)


class CreateSubject(CreateView):
    '''View for creating a new subject.
    '''
    model = Subject
    form_class = SubjectForm
    template_name = 'user/create_subject.html'

    def form_valid(self, form):
        # Save the new Subject record
        subject = form.save()
        # Also create a new Lendee record
        lendee = Lendee.objects.create(subject=subject)
        return super(CreateSubject, self).form_valid(form)


    def get_success_url(self):
        '''If the user came from the device checkin page,
        returns the user to that page. Otherwise, returns the
        user to the device index.'''
        if self.request.session['last_device_id']:
            return reverse_lazy('devices:checkout', kwargs={'pk': self.request.session['last_device_id']})
        else:
            return reverse_lazy('devices:index')


    