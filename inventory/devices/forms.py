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
        self.helper.form_id = 'deviceForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        super(DeviceForm, self).__init__(*args, **kwargs)