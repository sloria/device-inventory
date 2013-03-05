from factory import Factory, SubFactory
from inventory.user.tests.factories import UserFactory
from inventory.devices.models import *
from django.utils import timezone

class DeviceFactory(Factory):
    FACTORY_FOR = Device

    name = 'iPad 4, 16GB, WiFi'
    status = Device.CHECKED_IN
    make = 'PD510LL/A iPad WiFi 16BG / Black'
    serial_number = 'DMRJM1XTF182'


class ExperimenterFactory(Factory):
    FACTORY_FOR = Experimenter

    user = SubFactory(UserFactory)

class ReaderFactory(Factory):
    FACTORY_FOR = Reader

    user = SubFactory(UserFactory)
    
