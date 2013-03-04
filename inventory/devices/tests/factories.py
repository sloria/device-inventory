from factory import Factory
from inventory.devices.models import Device
from django.utils import timezone

class DeviceFactory(Factory):
    FACTORY_FOR = Device

    name = 'iPad 4, 16GB, WiFi'
    status = Device.CHECKED_IN
    make = 'PD510LL/A iPad WiFi 16BG / Black'
    serial_number = 'DMRJM1XTF182'