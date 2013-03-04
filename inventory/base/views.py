""" Views for the base application """

from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm

def home(request):
    """ Default view for the root """

    if request.user.is_authenticated():
        return redirect('devices:index', permanent=False)
    else:
        return render(request, 'registration/login.html', {'form': AuthenticationForm})
