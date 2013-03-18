from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *

from inventory.user.models import Experimenter, Reader

class UserForm(forms.Form):
    '''Form for creating a new User.
    '''
    USER_TYPE_CHOICES = (
                            ('admin', 'Admin'),
                            ('experimenter', 'Experimenter'),
                            ('reader', 'Reader')
                        )

    user_type = forms.ChoiceField(widget=forms.RadioSelect,
                                    choices=USER_TYPE_CHOICES,
                                    required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password',
                                max_length=30, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Password (again)',
                                max_length=30, required=True)

    def clean_email(self):
        '''Check if user with this email already exists.
        '''
        try:
            User.objects.get(email=self.cleaned_data['email'])
        except User.DoesNotExist:
            return self.cleaned_data['email']

    def clean(self):
        '''Check that password1 and password2 match.
        '''
        # Check initial validation
        if 'password1' and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Passwords don't match.")
        return self.cleaned_data

    def save(self):
        '''Create the user of the specified user type.
        '''
        # Create the new user. Note: The username is the email address
        new_user = User.objects.create_user(username=self.cleaned_data['email'],
                                            email=self.cleaned_data['email'],
                                            password=self.cleaned_data['password1'])
        new_user.first_name = self.cleaned_data['first_name']
        new_user.last_name = self.cleaned_data['last_name']

        # Create the user object of the specified type
        user_type = self.cleaned_data['user_type']
        new_user.save()
        if user_type == 'admin':
            new_user.is_superuser = True
            new_user.save()
        elif user_type == 'experimenter':
            return Experimenter.objects.create(user=new_user)
        elif user_type == 'reader':
            return Reader.objects.create(user=new_user)
        return new_user

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'user_form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        super(UserForm, self).__init__(*args, **kwargs)