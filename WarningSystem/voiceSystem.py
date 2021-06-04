import pyttsx3
import config

FEMALE = 0
GENERAL_WARNING = 2


class VoiceSystem:

    def __init__(self, indices_list):
        """
        init indices & msgs & the model for text to speech msgs
        given the teacher an option to to give us unique messages for the student.
        :param indices_list: list of indices the student failed in
        """
        self.indices_list = indices_list
        self.indices_msgs = self.__init_indices_msgs() if config.TEACHER_MSGS is None else config.TEACHER_MSGS
        self.msg = ''
        self.general_msg = ' Please return to learning mode!.'
        # Object voice creation.
        self.engine = pyttsx3.init()
        self.__init_msg()
        self.__set_voice()
        self.__debug_voice() if config.DEBUG else None
        self.__run_voice_system()

    @staticmethod
    def __init_indices_msgs():
        """
        create a dictionary of indices and their appropriate msgs if
        the student failed in those indices.
        :return: indices_msgs: a general msgs to the voice system.
        """
        indices_msgs = {
            'FACEDETECTOR': 'Our system suspects you are not in front of the screen.',
            'HEADPOSE': 'Our system notes that you are not looking at the screen.',
            'ONTOP': 'Our system detected that you are running non-lesson related apps.',
            'OBJECTDETECTOR': 'Our system detected that you are dealing with distracting objects.',
            'SLEEPDETECTOR': 'Our system suspects you\'m asleep',
            'FACERECOGNITION': 'Our system suspects that you are not the person in front of the screen.',
            'MANY_FAILURES': 'Our system updates that you are completely out of learning mode.'
        }
        return indices_msgs

    def __init_msg(self):
        """
        initialize the messages into a one long string for the voice model.
        """
        if len(self.indices_list) > GENERAL_WARNING:
            self.msg = self.indices_msgs['MANY_FAILURES']
            return
        for i in self.indices_list:
            if i != 'SPEAKER':
                self.msg += self.indices_msgs[i] + ' '

    def __run_voice_system(self):
        """
        run the voice system & if in debug mode, record the voice system
        into a mp3 file.
        """
        self.engine.say(self.msg)
        self.engine.say(self.general_msg)
        self.engine.runAndWait()
        if config.DEBUG:
            self.engine.save_to_file(self.msg + self.general_msg, '.\\Mp3Files\\test.mp3')
            self.engine.runAndWait()
        self.engine.stop()

    def __debug_voice(self):
        """
        while in debug mode, print all the details about the
        voice model.
        """
        # RATE: getting details of current speaking rate.
        rate = self.engine.getProperty('rate')
        # Printing current voice rate.
        print(rate)
        # VOLUME: getting details of the current volume level (maximum=1, minimum=0).
        volume = self.engine.getProperty('volume')
        # Printing the current volume level.
        print(volume)
        # VOICE: getting details of the current voice (male=1, female=0).
        voice = self.engine.getProperty('voice')
        # Printing the current voice.
        print(voice)

    def __set_voice(self):
        """
        set the voice model properties.
        """
        self.engine.setProperty('rate', 180)
        self.engine.setProperty('volume', 1)
        self.engine.setProperty('voice', self.engine.getProperty('voices')[not FEMALE].id)


def for_tests_only():
    """
    this function is used only for tests.
    """
    indices_list = ['FACEDETECTOR', 'OBJECTDETECTOR', 'SLEEPDETECTOR']
    VoiceSystem(indices_list)
    indices_list = ['FACERECOGNITION', 'OBJECTDETECTOR']
    VoiceSystem(indices_list)


if __name__ == '__main__':
    for_tests_only()
