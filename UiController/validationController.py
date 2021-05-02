import random
import config
from EmailMessagingSystem import emailSystem as es
from Services import httpService as hs
import re

LEN_CODE = 6
REGEX = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


class ValidationController:

    def __init__(self):
        """
        initialize the validation controller.
        """
        self.code = random.randint(10 ** (LEN_CODE - 1), 10 ** LEN_CODE - 1)

    @staticmethod
    def check_email(email):
        """
        check email structure.
        :param email: the email address to check
        :return: string that indicate if email is valid
        """
        return 'Invalid Email' if not re.search(REGEX, email) else 'OK'

    def check_code(self, code):
        """
        check the code to know if it the code we sent to the student.
        :param code: the code to check
        :return: string that indicate if the code is valid
        """
        if len(code) != LEN_CODE:
            return 'Code need to be in len: ' + str(LEN_CODE) + '.'
        if not code.isnumeric():
            return 'Code need to be only numbers.'
        if code != str(self.code):
            return 'This is not the correct code.'
        return 'OK'

    def send_email_to_server(self, email):
        """
        after email validation send the email to the server.
        :param email: the email to send to the server
        """
        # TODO - send email to database & delete the two lines below [if config.DEBUG]
        config.EMAIL['USER_EMAIL'] = email
        if config.DEBUG:
            return
        hs.post('url/gh', config.EMAIL['USER_EMAIL'])

    def send_validation_email(self, email):
        """
        send the validation email with the validation code to the student.
        :param email: the email address to send
        :return: bool indicating if the email sent
        """
        msg = """\
                Subject: TheBackEye Validation Code

                    This is your validation code:
                    """ + str(self.code) + """
                    please enter this code in the app.

                TheBackEye Team
                """
        return es.EmailSystem().send_email(msg, email)
