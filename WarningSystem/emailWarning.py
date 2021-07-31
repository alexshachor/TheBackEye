import config
from EmailMessagingSystem import emailSystem as es


class EmailWarning:

    def __init__(self, failed_measurements, user_email):
        """
        init the email msg & email user
        :param: failed_measurements: list of failed measurements
        """
        self.__msg = self.__create_msg(failed_measurements)
        self.__user_email = user_email
        self.__subject = 'TheBackEye Warning System!'
        self.__send_msg()

    @staticmethod
    def __create_msg(failed_measurements):
        tmp_msg = ''
        if 'ObjectDetector'.upper() in failed_measurements:
            tmp_msg += 'Our system detected that you are messing with your cell phone,\n'
        if 'SoundCheck'.upper() in failed_measurements:
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
        es.EmailSystem().send_email(self.__subject, self.__msg, self.__user_email)


def for_tests_only():
    """
    A test func to this page only.
    """
    EmailWarning(['OBJECTDETECTOR', 'SoundCheck'],"TheBackEyeApp@gmail.com")


if __name__ == '__main__':
    for_tests_only()
