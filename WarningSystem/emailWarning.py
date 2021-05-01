import config
from EmailMessagingSystem import emailSystem as es


class EmailWarning:

    def __init__(self):
        self.__msg = """\
            Subject: TheBackEye Warning

            Our system detected that you are messing with your cell phone,
            please return to learning mode.

            TheBackEye Team
            """
        self.__user_email = config.EMAIL['USER_EMAIL']
        self.__send_msg()

    def __send_msg(self):
        es.EmailSystem().send_email(self.__msg, self.__user_email)


def for_tests_only():
    pass


if __name__ == '__main__':
    for_tests_only()
