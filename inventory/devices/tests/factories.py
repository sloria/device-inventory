from factory import Factory, Sequence
from inventory.devices.models import Device

class IpadFactory(Factory):
    FACTORY_FOR = Device

    name = "iPad"
    description = 'iPad 4, 16GB, WiFi'
    status = Device.CHECKED_IN_NOT_READY
    make = 'PD510LL/A iPad WiFi 16BG / Black'
    serial_number = Sequence(lambda n: 'DMRJM1XTF182{0}'.format(n))

class HeadphonesFactory(Factory):
    FACTORY_FOR = Device
    name = "Headphones"
    description = 'white headphones'
    status = Device.CHECKED_IN_NOT_READY
    make = "iPad headphones"

class AdapterFactory(Factory):
    FACTORY_FOR = Device
    name = 'Power adapter'
    description = "wall charger adapter"
    make = "iPad wall charger adapter"

class CaseFactory(Factory):
    FACTORY_FOR = Device
    name = 'iPad case'
    description = "Case for the iPad, blue"
    make = "iPad case"

def create_device_factories():
    (ipad, headphones, 
        adapter, case) = (IpadFactory(),
                            HeadphonesFactory(),
                            AdapterFactory(),
                            CaseFactory())
    return ipad, headphones, adapter, case