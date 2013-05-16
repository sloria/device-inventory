from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *

from inventory.comments.models import (IpadComment,
    AdapterComment, HeadphonesComment, CaseComment)


class CommentUpdateForm(forms.ModelForm):
    '''Form for updating a comment.
    '''
    text = forms.CharField(label='Comment: ', widget=forms.Textarea,
                             max_length=500, required=True)
    class Meta:
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
        return super(CommentUpdateForm, self).__init__(*args, **kwargs)

class IpadCommentUpdateForm(CommentUpdateForm):
    class Meta:
        model = IpadComment
        fields = ('text',)