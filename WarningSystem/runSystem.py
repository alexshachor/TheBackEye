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
        # assign all processes and start each one of them
        if not self.failed_in:
            return
        processes = []

        for key, process in self.dict_process.items():
            if key == 'email':
                if 'ObjectDetector'.upper() in self.failed_in:
                    process.start()
                    processes.append(process)
            else:
                process.start()
                processes.append(process)

        for process in processes:
            process.join()
            process.close()

    def __init_failed_indices(self):
        for key, val in self.indices_dict.items():
            if not val:
                self.failed_in.append(key.upper())


def for_tests_only():
    indices_dict = {
        'FaceDetector': True, 'ObjectDetector': False, 'SleepDetector': True,
        'OnTop': False, 'HeadPose': True
    }
    RunSystem(indices_dict)


if __name__ == '__main__':
    for_tests_only()

