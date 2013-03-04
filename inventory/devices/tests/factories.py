from factory import Factory
from inventory.devices.models import Device

class DeviceFactory(Factory):
    FACTORY_FOR = Device
    name = 'iPad 4, 16GB, WiFi'
    status = 'Checked in'
