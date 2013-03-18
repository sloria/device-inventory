from factory import Factory, Sequence
from inventory.devices.models import Device

class DeviceFactory(Factory):
    FACTORY_FOR = Device

    name = 'iPad 4, 16GB, WiFi'
    status = Device.CHECKED_IN
    make = 'PD510LL/A iPad WiFi 16BG / Black'
    serial_number = Sequence(lambda n: 'DMRJM1XTF182{0}'.format(n))
