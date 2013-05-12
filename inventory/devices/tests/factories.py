from factory import Factory, Sequence
from inventory.devices.models import *

class IpadFactory(Factory):
    FACTORY_FOR = Ipad

    name = "iPad"
    description = 'iPad 4, 16GB, WiFi'
    status = Device.CHECKED_IN_NOT_READY
    make = 'PD510LL/A iPad WiFi 16BG / Black'
    serial_number = Sequence(lambda n: 'DMRJM1XTF182{0}'.format(n))

class HeadphonesFactory(Factory):
    FACTORY_FOR = Headphones
    description = 'white headphones'
    status = Device.CHECKED_IN
    make = "iPad headphones"

class AdapterFactory(Factory):
    FACTORY_FOR = Adapter
    name = 'Power adapter'
    description = "wall charger adapter"
    make = "iPad wall charger adapter"

class CaseFactory(Factory):
    FACTORY_FOR = Case
    name = 'iPad case'
    description = "Case for the iPad, blue"
    make = "iPad Smartcase"

def create_device_factories():
    (ipad, headphones, 
        adapter, case) = (IpadFactory(),
                            HeadphonesFactory(),
                            AdapterFactory(),
                            CaseFactory())
    return ipad, headphones, adapter, case