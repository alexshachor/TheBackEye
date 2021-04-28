import multiprocessing as mp
from WarningSystem import voiceSystem as vs
from WarningSystem import flickerSystem as fs
from WarningSystem import emailWarning as ew


class RunSystem:

    def __init__(self, indices_dict):
        self.indices_dict = indices_dict
        self.failed_in = []
        self.dict_process = {
            'voice': mp.Process(target=vs.VoiceSystem, args=(self.failed_in,)),
            'flicker': mp.Process(target=fs.FlickerSystem),
            'email': mp.Process(target=ew.EmailWarning)
        }
        self.__init_failed_indices()
        self.__run_warning_system()

    def __run_warning_system(self):
        pass

    def __init_failed_indices(self):
        pass


def for_tests_only():
    pass


if __name__ == '__main__':
    for_tests_only()

