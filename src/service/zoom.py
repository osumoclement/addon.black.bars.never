import xbmc
import time
from src.core import core
from src.content import ContentManager
from src.player import Player

class ZoomService:
    def __init__(self):
        self.player = Player()
        self.content = ContentManager(self.player)
        self.player.set_onAVStarted_callback(self.start_service)
        self.auto_refresh_status = False

    def reset_attributes(self):
        self.auto_refresh_status = False
        core.logger.on()
        core.notification.on()
        self.content.reset_attributes()
        self.player.reset_attributes()

    def start_service(self):
        if not core.addon.get_setting("automatically_execute", bool) or core.window.get_property("processing"):
            return
        
        core.window.set_property("processing", True)
        core.window.set_property("status", True)
        
        try:
            self.reset_attributes()

            # Fetch IMDb metadata if multi-aspect ratios support is enabled or Android workaround is active
            if core.addon.get_setting("multi_aspect_ratios_support", bool) or core.addon.get_setting("android_workaround", bool):
                self.content.fetch_online_metadata()

            if self.content.multi_ar:
                core.notification.notify("Multiple aspect ratios detected", override=True)

            self.auto_refresh_status = (self.content.multi_ar and not core.addon.get_setting("android_workaround", bool)) or core.addon.get_setting("always_refresh", bool)

            if self.auto_refresh_status:
                self.auto_refresh_zoom()
            else:
                self.execute_zoom()
        except Exception as e:
            core.logger.log(e, xbmc.LOGERROR)
            
        core.window.clear_property("processing")

    def check_toggle_service(self, status: str):
        if status == "on":
            if core.window.get_property("toggle_on"):
                    self.start_service()
                    core.window.clear_property("toggle_on")
                    return True
        elif status == "off":
            if core.window.get_property("toggle_off"):
                    self.off_zoom()
                    core.window.clear_property("toggle_off")
                    return True
        return False

    def auto_refresh_zoom(self):
        refresh_interval = core.addon.get_setting("refresh_interval", int)
        check_interval = 1  # How often to check the conditions in seconds

        while not core.monitor.abortRequested() and self.player.isPlayingVideo() and self.auto_refresh_status:
            self.execute_zoom()
            core.notification.off()
            core.logger.off()

            start_time = time.time()  # Record start time of the interval

            while True:
                current_time = time.time()
                elapsed = current_time - start_time
                remaining_time = refresh_interval - elapsed

                if self.check_toggle_service("off"):
                    break
                
                if remaining_time <= 0:
                    break  # Break immediately if the interval has completed
                
                # Use waitForAbort for the remaining time or the check interval, whichever is shorter
                if core.monitor.waitForAbort(min(remaining_time, check_interval)):
                    break  # Exit if waitForAbort returns True (Kodi is requesting an abort)
            
            if core.monitor.abortRequested():
                break
        
        core.logger.log("Exiting auto refresh zoom loop.", xbmc.LOGINFO)

    def execute_zoom(self):
        zoom_amount = self._calculate_zoom()

        if zoom_amount is None:
            core.logger.log("Unable to calculate zoom", xbmc.LOGERROR)
            core.notification.notify("Unable to calculate zoom", override=True)
            return
        
        # Execute the zoom via JSON-RPC
        xbmc.executeJSONRPC(
                '{"jsonrpc": "2.0", "method": "Player.SetViewMode", "params": {"viewmode": {"zoom": ' + str(zoom_amount) + ' }}, "id": 1}'
            )
        
        core.window.set_property("status", False)
        
        if zoom_amount > 1.0:
            core.notification.notify(f"Adjusted zoom to {zoom_amount}")

    def off_zoom(self):
        self.reset_attributes()

        xbmc.executeJSONRPC(
            '{"jsonrpc": "2.0", "method": "Player.SetViewMode", "params": {"viewmode": {"zoom": 1.0' + ' }}, "id": 1}'
        )
        core.window.set_property("status", False)
        core.notification.notify("Showing original aspect ratio", override=True)

    def toggle_zoom(self):
        if not self.player.isPlayingVideo():
            core.notification.notify("No video playing.", override=True)
            return
        
        if core.window.get_property("status"):
            core.window.set_property("toggle_off", True)
        else:
            core.window.set_property("toggle_on", True)

    def _calculate_zoom(self):
        content_width, content_height = self.content.get_content_size()

        if content_width is None or content_height is None:
            return None
        
        content_ar = self.content.get_content_ar()
        core.logger.log(f"Content Dimension: {content_width:.2f}x{content_height:.2f}, Content Aspect Ratio: {content_ar:.2f}:1", level=xbmc.LOGINFO)

        monitor_width, monitor_height = self.player.get_monitor_size()
        monitor_ar = self.player.get_monitor_ar()
        core.logger.log(f"Monitor Size: {monitor_width}x{monitor_height}", level=xbmc.LOGINFO)

        if content_ar < monitor_ar:
            # Fill to height
            zoom_amount = round(float(monitor_height) / content_height, 2)
        else:
            # Fill to width
            zoom_amount = round(float(monitor_width) / content_width, 2)

        core.logger.log(f"Zoom amount: {zoom_amount}", level=xbmc.LOGINFO)
        return zoom_amount