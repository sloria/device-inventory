from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from inventory.devices.models import Device

class DeviceForm(forms.ModelForm):
    '''Form for creating a new device.
    '''
    class Meta:
        model = Device
        fields = ('name', 'description', 'responsible_party', 'make', 'serial_number',
                    'purchased_at')

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'device_form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        super(DeviceForm, self).__init__(*args, **kwargs)

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

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'checkin_form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        super(CheckinForm, self).__init__(*args, **kwargs)