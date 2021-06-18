import config
from EmailMessagingSystem import emailSystem as es


class EmailWarning:

    def __init__(self, failed_measurements):
        """
        init the email msg & email user
        :param: failed_measurements: list of failed measurements
        """
        self.__msg = self.__create_msg(failed_measurements)
        self.__user_email = config.EMAIL['USER_EMAIL']
        self.subject = 'TheBackEye Warning System!'
        self.__send_msg()

    @staticmethod
    def __create_msg(map_measurements):
        tmp_msg = ''
        if 'ObjectDetector'.upper() in map_measurements:
            tmp_msg += 'Our system detected that you are messing with your cell phone,\n'
        if 'Speaker'.upper() in map_measurements:
            tmp_msg += 'Our system detected that your speaker turned off,\n'
        msg = """\
            Hi
            """ + tmp_msg + """
            please return to learning mode.

            TheBackEye Team
            """
        return msg

    def __send_msg(self):
        """
        send the email to the user via EmailSystem
        """
        es.EmailSystem().send_email(self.subject, self.__msg, self.__user_email)


def for_tests_only():
    """
    A test func to this page only.
    """
    EmailWarning(['OBJECTDETECTOR', 'SPEAKER'])


if __name__ == '__main__':
    for_tests_only()
