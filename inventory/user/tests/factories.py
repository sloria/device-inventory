import factory

from django.contrib.auth.models import User

class UserFactory(factory.Factory):
    FACTORY_FOR = User

    username = factory.Sequence(lambda n: "user{0}@example.com".format(n))
    password = 'abc'
    is_active = True

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
            if create:
                user.save()
        return user