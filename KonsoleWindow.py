from dbus.bus import BusConnection
import dbus

class KonsoleWindow:

    def __init__(self, konsole_service_name, bus: BusConnection):
        self.sessions = {}
        self.last_current_session = ''
        self.window_service = dbus.Interface(bus.get_object(konsole_service_name, '/Windows/1'), 'org.kde.konsole.Window')

        def on_update(*args):
            current_session_id = str(self.window_service.currentSession())
            if self.last_current_session == current_session_id:
                return
            # Update sessions
            existing_sessions = set(self.window_service.sessionList())
            # Remove
            for removed_session in self.sessions.keys() - existing_sessions:
                del self.sessions[removed_session]
            # Add
            for new_session in existing_sessions - self.sessions.keys():
                self.sessions[new_session] = dbus.Interface(
                    bus.get_object(konsole_service_name, f'/Sessions/{new_session}'), 'org.kde.konsole.Session')

            for session_id, session in self.sessions.items():
                session.setProfile('active' if session_id == current_session_id else 'inactive')
            self.last_current_session = current_session_id

        self.listener = bus.add_signal_receiver(on_update, 'ItemsPropertiesUpdated', 'com.canonical.dbusmenu', konsole_service_name, '/MenuBar/1')


    def __del__(self):
        self.listener.remove()
