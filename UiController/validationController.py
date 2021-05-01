import random
import config
from EmailMessagingSystem import emailSystem as es
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
        pass

    def send_email_to_server(self, email):
        pass

    def send_validation_email(self, email):
        pass
