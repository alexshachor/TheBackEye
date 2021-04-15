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
        pass

    def check_and_act(self):
        pass

    def is_in_good_size(self):
        pass

    def handle_active_teacher(self, is_on_top):
        pass

    def __repr__(self):
        return 'OnTop'