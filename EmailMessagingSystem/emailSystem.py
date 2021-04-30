import smtplib
import ssl
import config
from Services import loggerService as ls


class EmailSystem:

    def __init__(self):
        self.sender = config.EMAIL['EMAIL']
        self.password = config.EMAIL['PASSWORD']
        self.port = 465
        self.success = False

    def send_email(self, msg, recipient_email):
        context = ssl.create_default_context()
        print("Starting to send") if config.DEBUG else None
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", self.port, context=context) as server:
                server.login(self.sender, self.password)
                server.sendmail(self.sender, recipient_email, msg)
                self.success = True
        except ValueError as v:
            ls.get_logger().error(str(v))
        except Exception as e:
            ls.get_logger().error(f'failed to send the email, due to: {str(e)}')
        print("sent email!") if config.DEBUG else None
        return self.success


def for_tests_only():
    x = EmailSystem()
    message = """\
    Subject: Python Email Test\n

    hi how are you.\n

    From Tests
    """
    x.send_email(message, "rshalom8@gmail.com")


if __name__ == '__main__':
    for_tests_only()
