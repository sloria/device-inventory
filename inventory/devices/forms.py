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
        self.helper.form_class = 'form-widget'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                    'Add device',
                    'name',
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
    comment = forms.CharField(label="Comment: ", widget=forms.Textarea,
                                    max_length=500,
                                    required=False)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'checkin_form'
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
        super(CheckinForm, self).__init__(*args, **kwargs)

class DeviceEditForm(forms.Form):
    '''Form for updating a device's attributes.
    '''

    def __init__(self, instance, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'edit_form'
        self.helper.form_class = "form-widget"
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                "Edit device",
            ),
            ButtonHolder(
                Submit('submit', "Submit")
            )
        )
        super(DeviceEditForm, self).__init__(instance, *args, **kwargs)

