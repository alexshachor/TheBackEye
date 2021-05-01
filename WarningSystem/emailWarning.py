import config
from EmailMessagingSystem import emailSystem as es


class EmailWarning:

    def __init__(self):
        """
        init the email msg & email user
        """
        self.__msg = """\
            Subject: TheBackEye Warning

            Our system detected that you are messing with your cell phone,
            please return to learning mode.

            TheBackEye Team
            """
        self.__user_email = config.EMAIL['USER_EMAIL']
        self.__send_msg()

    def __send_msg(self):
        """
        send the email to the user via EmailSystem
        """
        es.EmailSystem().send_email(self.__msg, self.__user_email)


def for_tests_only():
    """
    A test func to this page only.
    """
    EmailWarning()


if __name__ == '__main__':
    for_tests_only()
