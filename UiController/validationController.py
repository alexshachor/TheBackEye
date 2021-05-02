import random
import config
from EmailMessagingSystem import emailSystem as es
from Services import httpService as hs
import re

LEN_CODE = 6
REGEX = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


class ValidationController:

    def __init__(self):
        self.code = random.randint(10 ** (LEN_CODE - 1), 10 ** LEN_CODE - 1)

    @staticmethod
    def check_email(email):
        return 'Invalid Email' if not re.search(REGEX, email) else 'OK'

    def check_code(self, code):
        if len(code) != 6:
            return 'Code need to be in len six.'
        if not code.isnumeric():
            return 'Code need to be only numbers.'
        if code != str(self.code):
            return 'This is not the correct code.'
        return 'OK'

    def send_email_to_server(self, email):
        # TODO - send email to database
        config.EMAIL['USER_EMAIL'] = email
        if config.DEBUG:
            return
        hs.post('url/gh', config.EMAIL['USER_EMAIL'])

    def send_validation_email(self, email):
        msg = """\
                Subject: TheBackEye Validation Code

                    This is your validation code:
                    """ + str(self.code) + """
                    please enter this code in the app.

                TheBackEye Team
                """
        return es.EmailSystem().send_email(msg, email)
