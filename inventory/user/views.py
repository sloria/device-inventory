# Create your views here.
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import FormView

from inventory.user.forms import UserForm

class UserAdd(FormView):
    '''View for adding a device.
    '''
    form_class = UserForm
    template_name = 'user/add.html'
    success_url = reverse_lazy('devices:index')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 
            'Successfully created user: {0}'.format(form.cleaned_data['email']))
        return super(UserAdd, self).form_valid(form)