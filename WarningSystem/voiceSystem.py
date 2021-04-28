import pyttsx3
import config


class VoiceSystem:

    def __init__(self, indices_list):
        self.indices_list = indices_list
        self.indices_msgs = self.__init_indices_msgs() if config.TEACHER_MSGS is None else config.TEACHER_MSGS
        self.msg = ''
        self.general_msg = ' Please return to learning mode!.'
        # Object voice creation.
        self.engine = pyttsx3.init()
        self.__init_msg()
        self.__set_vice()
        self.__debug_voice() if config.DEBUG else None
        self.__run_voice_system()

    @staticmethod
    def __init_indices_msgs():
        pass

    def __init_msg(self):
        pass

    def __run_voice_system(self):
        pass

    def __debug_voice(self):
        pass

    def __set_vice(self):
        pass


def for_tests_only():
    pass


if __name__ == '__main__':
    for_tests_only()
