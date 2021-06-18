import os
import platform


class ZoomService:

    def __init__(self, link):
        self.link = link
        self.domain_name, self.password, self.code = self.__decode_link()

    def join(self):
        if platform.system() == 'Windows':
            command = f'start {self.link}' if self.code == "NOT FOUND" else \
                f'start zoommtg://{self.domain_name}/join?confno={self.code}?"&"pwd={self.password}'
        else:
            command = f'open {self.link}' if self.code == "NOT FOUND" else \
                f'open "zoommtg://{self.domain_name}/join?confno={self.code}?&pwd={self.password}"'
        os.system(command)

    @staticmethod
    def quit():
        if platform.system() == 'Windows':
            os.system('taskkill /f /im Zoom.exe')
        else:
            os.system('killall zoom.us')

    def __decode_link(self):
        pass


def for_tests_only():
    pass


if __name__ == '__main__':
    for_tests_only()
