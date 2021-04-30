import config


class EmailSystem:

    def __init__(self):
        self.sender = config.EMAIL['EMAIL']
        self.password = config.EMAIL['PASSWORD']
        self.port = 465
        self.success = False

    def send_email(self, msg, recipient_email):
        pass


def for_tests_only():
    pass


if __name__ == '__main__':
    for_tests_only()
