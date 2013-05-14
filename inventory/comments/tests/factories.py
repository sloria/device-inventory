'''Factories for device comments.'''
from factory import Factory, SubFactory
from inventory.comments.models import (IpadComment, 
    HeadphonesComment, AdapterComment, CaseComment)
from inventory.devices.tests.factories import (IpadFactory, 
    HeadphonesFactory, AdapterFactory, CaseFactory)
from inventory.user.tests.factories import UserFactory

class IpadCommentFactory(Factory):
    FACTORY_FOR = IpadComment
    device = SubFactory(IpadFactory)
    text = "All good here."
    user = SubFactory(UserFactory)

class HeadphonesCommentFactory(Factory):
    FACTORY_FOR = HeadphonesComment
    device = SubFactory(HeadphonesFactory)
    text = "Beats be bumpin."
    user = SubFactory(UserFactory)

class AdapterCommentFactory(Factory):
    FACTORY_FOR = AdapterComment
    device = SubFactory(AdapterFactory)
    text = "It gives power!"
    user = SubFactory(UserFactory)

class CaseCommentFactory(Factory):
    FACTORY_FOR = CaseComment
    device = SubFactory(CaseFactory)
    text = "Case closed."
    user = SubFactory(UserFactory)

def create_comment_factories():
    '''Return a tuple of factory instances of each comment model.
    '''
    all_comments = (IpadCommentFactory(),
                    HeadphonesCommentFactory(),
                    AdapterCommentFactory(),
                    CaseCommentFactory())
    return all_comments
