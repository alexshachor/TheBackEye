import os
import platform


class ZoomService:

    def __init__(self, link):
        """
        init all the needed parameters to automatically join zoom meeting
        :param link: a fool link to zoom meeting
        """
        self.__link = link
        self.__domain_name, self.__password, self.__code = self.__decode_link()

    def join(self):
        """
        auto join zoom meeting
        """
        if platform.system() == 'Windows':
            command = f'start {self.__link}' if self.__code == "NOT FOUND" else \
                f'start zoommtg://{self.__domain_name}/join?confno={self.__code}?"&"pwd={self.__password}'
        else:
            command = f'open {self.__link}' if self.__code == "NOT FOUND" else \
                f'open "zoommtg://{self.__domain_name}/join?confno={self.__code}?&pwd={self.__password}"'
        os.system(command)

    @staticmethod
    def quit():
        """
        function to quit the zoom meeting
        """
        if platform.system() == 'Windows':
            os.system('taskkill /f /im Zoom.exe')
        else:
            os.system('killall zoom.us')

    def __decode_link(self):
        """
        extract meeting info from zoom url.
        :return: domain_name: domain name
        :return: password: password of the zoom meeting
        :return: code: conference code
        """
        try:
            password = self.__link.split('pwd=')[1]
        except:
            password = ''
        try:
            code = self.__link.split('/j/')[1].split('?pwd=')[0]
        except:
            code = "NOT FOUND" if code == "" else code.strip()
        try:
            domain_name = self.__link.split("//")[1].split("/j")[0]
        except:
            domain_name = ''
        return domain_name, password, code


def for_tests_only():
    """
    A test func to this page only.
    """
    meeting = ZoomService('https://us04web.zoom.us/j/79870014162?pwd=TklmK2hJNVhoUElxWHBVRzlTdnpCdz09')
    meeting.join()


if __name__ == '__main__':
    for_tests_only()
