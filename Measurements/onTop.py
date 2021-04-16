from Measurements import abstractMeasurement as am
from Services import loggerService as ls
from config import DESIRED_PROGRAM
import win32gui as w
import psutil
import win32process
import win32con
from win32api import GetSystemMetrics

# If it False: If the desired program is not ON TOP, it will be.
# If it True: Report only.
REPORT_ONLY = False
# The volume that a program considered to be On Top.
DESIRED_SIZE = 77


class OnTop(am.AbstractMeasurement):

    def __init__(self):
        am.AbstractMeasurement.__init__(self)
        self.screen_width = GetSystemMetrics(0)
        self.screen_height = GetSystemMetrics(1)

    def run(self, frame, dict_results):
        result = {repr(self): False}
        try:
            am.AbstractMeasurement.run(self, frame, dict_results)
            result[repr(self)] = self.check_and_act()
        except Exception as e:
            ls.get_logger().error(
                f'Failed to identify which program on top, due to: {str(e)}')
            dict_results.update(result)
            return
        dict_results.update(result)

    def check_and_act(self):
        # Check which program is on top.
        program_name = None
        is_on_top = False
        try:
            pid = win32process.GetWindowThreadProcessId(w.GetForegroundWindow())
            program_name = psutil.Process(pid[-1]).name().lower()
        except Exception as e:
            ls.get_logger().error(
                f'Failed to identify process up front, due to: {str(e)}')
        if program_name == DESIRED_PROGRAM['EXPECTED_ON_TOP']:
            is_on_top = True
            if self.is_in_good_size():
                return True
        # If we got here the student is not watching the desired program and we act
        # according to the settings.
        if not REPORT_ONLY:
            self.handle_active_teacher(is_on_top)
        return False

    def is_in_good_size(self):
        rect = w.GetWindowRect(w.GetForegroundWindow())
        x, y = rect[0], rect[1]
        width, height = rect[2] + x if x < 0 else rect[2] - x, rect[3] - y
        screen_volume = self.screen_width * self.screen_height
        foreground_window_volume = width * height
        accepted_percentage = ((100 - DESIRED_SIZE) * screen_volume) / 100
        if screen_volume - foreground_window_volume < accepted_percentage:
            return True
        return False

    def handle_active_teacher(self, is_on_top):
        pass

    def __repr__(self):
        return 'OnTop'
