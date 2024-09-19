from dbus.bus import BusConnection

class KonsoleWindow:

    listener = None
    sessions = {}

    def __init__(self, konsole_service_name, bus: BusConnection):
        self.listener = bus.add_signal_receiver(lambda x, y: print(x, y), 'ItemsPropertiesUpdated', 'com.canonical.dbusmenu', konsole_service_name, '/MenuBar/1')


    def __del__(self):
        self.listener.remove()
