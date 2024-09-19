#!/usr/bin/python3
from KonsoleWindow import KonsoleWindow
import dbus
from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop

class Main:
    konsole_windows = {}
    bus = None

    def add_konsole(self, konsole_name):
        konsole = KonsoleWindow(konsole_name, self.bus)
        self.konsole_windows[konsole_name] = konsole
        print(f"ajout {konsole_name}")


    def remove_konsole(self, konsole_name):
        self.konsole_windows.pop(konsole_name)
        print(f"suppression {konsole_name}")


    def __init__(self):
        DBusGMainLoop(set_as_default=True)
        loop = GLib.MainLoop()
        self.bus = dbus.SessionBus()

        # Add existing Konsole windows at startup
        dbus_service = dbus.Interface(self.bus.get_object('org.freedesktop.DBus', '/'),  'org.freedesktop.DBus')
        for konsole in list(filter(lambda service: 'org.kde.konsole-' in service, dbus_service.ListNames())):
            self.add_konsole(konsole)


        # Listen for new Konsole windows and add them
        def on_name_owner_change(name: str, old_owner: str, new_owner: str):
            if not name.startswith('org.kde.konsole'):
                return
            if old_owner == '':
                self.add_konsole(name)
            elif new_owner == '':
                self.remove_konsole(name)

        (dbus.Interface(self.bus.get_object('org.freedesktop.DBus', '/org/freedesktop/DBus'), 'org.freedesktop.DBus')
         .connect_to_signal('NameOwnerChanged', on_name_owner_change))

        # Main loop
        loop.run()


Main()
