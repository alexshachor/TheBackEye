import multiprocessing as mp
from WarningSystem import voiceSystem as vs
from WarningSystem import flickerSystem as fs
from WarningSystem import emailWarning as ew


class RunSystem:

    def __init__(self, indices_dict):
        """
        initialize the indices & the processes that are related
        to the warning system.
        :param indices_dict: dictionary of indices
        """
        self.__indices_dict = indices_dict
        self.__failed_in = []
        self.__dict_process = {
            'voice': mp.Process(target=vs.VoiceSystem, args=(self.__failed_in,)),
            'flicker': mp.Process(target=fs.FlickerSystem),
            'email': mp.Process(target=ew.EmailWarning, args=(self.__failed_in,))
        }
        self.__init_failed_indices()
        self.__run_warning_system()

    def __run_warning_system(self):
        """
        run the warning system in parallel.
        """
        # assign all processes and start each one of them
        if not self.__failed_in:
            return
        processes = []

        for key, process in self.__dict_process.items():
            if key == 'email':
                if 'ObjectDetector'.upper() in self.__failed_in or 'SoundCheck'.upper() in self.__failed_in:
                    process.start()
                    processes.append(process)
            else:
                process.start()
                processes.append(process)

        for process in processes:
            process.join()
            process.close()

    def __init_failed_indices(self):
        """
        initialize the indices that the student failed in.
        """
        for key, val in self.__indices_dict.items():
            if not val:
                self.__failed_in.append(key.upper())


def for_tests_only():
    """
    this function is used only for tests.
    """
    indices_dict = {
        'FaceDetector': True, 'ObjectDetector': False, 'SleepDetector': True,
        'OnTop': True, 'HeadPose': True, 'SoundCheck': False
    }
    RunSystem(indices_dict)


if __name__ == '__main__':
    for_tests_only()

