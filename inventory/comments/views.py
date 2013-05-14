from django.views.generic import View, UpdateView
from django.utils import simplejson as json
from django.contrib import messages
from django.http import HttpResponse

from inventory.comments.models import (IpadComment, HeadphonesComment,
            AdapterComment, CaseComment)
from inventory.comments.forms import CommentUpdateForm

class CommentDeleteView(View):
    '''An abstract CommentDelete View.'''

    def get_comment_class(self):
        """Returns the comment class corresponding to a 
        specific device type. Must be implemented by descendant classes.
        
        Example:
            return IpadComment
        """
        raise NotImplementedError

    def post(self, request, device_id, comment_id):
        response_data = {}
        # Delete the comment
        comment_class = self.get_comment_class()
        comment_class.objects.filter(pk=comment_id).delete()
        # Display a message
        messages.success(request, 'Successfully deleted comment.')
        response_data['success'] = True
        response_data['pk'] = comment_id
        json_data = json.dumps(response_data)
        return HttpResponse(json_data, mimetype='application/json')

class CommentUpdateView(UpdateView):
    '''An abstract CommentEdit View.'''
    template_name = 'devices/edit_comment.html'
    # Must define the comment model to update, like so:
    # model = IpadComment
    form_class = CommentUpdateForm
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        """On success, redirect to the device's detail page."""
        comment = self.get_object()
        return comment.device_url


class IpadCommentDelete(CommentDeleteView):
    def get_comment_class(self):
        return IpadComment

class IpadCommentUpdate(CommentUpdateView):
    model = IpadComment

class HeadphonesCommentDelete(CommentDeleteView):
    def get_comment_class(self):
        return HeadphonesComment

class HeadphonesCommentUpdate(CommentUpdateView):
    model = HeadphonesComment

class AdapterCommentDelete(CommentDeleteView):
    def get_comment_class(self):
        return AdapterComment

class AdapterCommentUpdate(CommentUpdateView):
    model = AdapterComment

class CaseCommentDelete(CommentDeleteView):
    def get_comment_class(self):
        return CaseComment

class CaseCommentUpdate(CommentUpdateView):
    model = CaseComment
