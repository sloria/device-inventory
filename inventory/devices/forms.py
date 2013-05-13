from django.utils import timezone
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from inventory.devices.models import *

class DeviceForm(forms.Form):
    '''Form for creating a new device.
    '''
    DEVICE_TYPES = (
                        ('ipad', 'iPad'),
                        ('headphones', 'Headphones'),
                        ('adapter', 'Power adapter'),
                        ('case', 'iPad case'),
                    )
    device_type = forms.ChoiceField(label='Device type: ', widget=forms.Select,
                                    choices=DEVICE_TYPES,
                                    required=True)

    description = forms.CharField(label='Description: ', widget=forms.Textarea,
                                    max_length=1000, help_text='Optional',
                                    required=False)

    responsible_party = forms.CharField(label='Responsible party: ',
                                    help_text='Optional',
                                    required=False)
    make = forms.CharField(label='Make: ')
    purchased_at = forms.DateField(label="Purchased at: ",
                                    initial=timezone.now(),
                                    required=False, help_text='Optional')
    serial_number = forms.CharField(label="Serial number: ",
                                    required=False, help_text='Optional')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'device_form'
        self.helper.form_class = 'form-widget'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                    'Add device',
                    'device_type',
                    'description',
                    'responsible_party',
                    'make',
                    'serial_number',
                    'purchased_at'
                ),
            ButtonHolder(
                    Submit('submit', 'Submit')
                )
        )
        return super(DeviceForm, self).__init__(*args, **kwargs)

class CheckinForm(forms.Form):
    '''Form for checking in a device.
    '''

    CONDITIONS = (
                    ('excellent', 'Excellent'),
                    ('scratched', 'Scratched'),
                    ('broken', 'Broken'),
                    ('missing', 'Missing')
                )



    condition = forms.ChoiceField(label='Condition: ', widget=forms.Select,
                                    choices=CONDITIONS,
                                    required=True)
    comment = forms.CharField(label="Comment: ", widget=forms.Textarea,
                                    max_length=500,
                                    required=False)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-checkin_form'
        self.helper.form_class = "form-widget"
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                "Check in",
                'condition',
                'comment',
            ),
            ButtonHolder(
                Submit('submit', "Submit")
            )
        )
        return super(CheckinForm, self).__init__(*args, **kwargs)

class DeviceUpdateForm(forms.ModelForm):
    '''Form for updating a device's attributes.
    '''

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-edit_form'
        self.helper.form_class = "form-widget"
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                "Edit device",
                'status',
                'name',
                'description',
                'make',
                'condition',
                'serial_number',
                'purchased_at',
                'created_at',
                'updated_at'
            ),
            ButtonHolder(
                Submit('submit', "Submit")
            )
        )
        return super(DeviceUpdateForm, self).__init__(*args, **kwargs)

class IpadUpdateForm(DeviceUpdateForm):
    class Meta:
        model = Ipad

class HeadphonesUpdateForm(DeviceUpdateForm):
    class Meta:
        model = Headphones

class AdapterUpdateForm(DeviceUpdateForm):
    class Meta:
        model = Adapter

class CaseUpdateForm(DeviceUpdateForm):
    class Meta:
        model = Case

class CommentEditForm(forms.ModelForm):
    '''Form for updating a comment.
    '''
    text = forms.CharField(label='Comment: ', widget=forms.Textarea,
                             max_length=500, required=True)
    class Meta:
        model = Comment 
        fields = ('text',)
    
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-edit_comment_form'
        self.helper.form_class = "form-widget"
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                "Edit comment",
                "text",
            ),
            ButtonHolder(
                Submit('submit', "Submit")
            )
        )
        return super(CommentEditForm, self).__init__(*args, **kwargs)
