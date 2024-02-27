import xbmc
import xbmcgui

class LoggingService():
    def __init__(self):
        self.status = True
        self.addon_name = None

    def set_config(self, config):
        self.config = config
        self.addon_name = self.config.get_addon_name()

    def on(self):
        self.status = True

    def off(self):
        self.status = False

    def get_status(self):
        return self.status

    def log(self, msg, level=xbmc.LOGINFO):
        if self.addon_name is None:
            raise ValueError("Addon name has not been set.")
        
        if self.get_status():
            xbmc.log(f"{self.addon_name}: {msg}", level=level)

class NotificationService():
    def __init__(self):
        self.status = True
        self.addon_name = None
        self.icon_path = None

    def set_config(self, config):
        self.config = config
        self.addon_name = self.config.get_addon_name()
        self.icon_path = self.config.get_addon_icon()

    def get_status(self):
        return self.status

    def notify(self, msg, override=False):
        self.status = self.config.get_setting("show_notification", bool)

        if self.addon_name is None:
            raise ValueError("Addon name has not been set.")
        
        if self.status or override:
            xbmcgui.Dialog().notification(self.addon_name, msg, self.icon_path, 1000)