import config
from Services import httpService


class StudentManager():
    """
    This class manages the student details that come from remote.
    """
    student = None

    def get_student(self, password=None):
        """
        Get specific student from remote
        :param params: params for the GET request (e.g: password)
        :return: configuration dictionary
        """
        if password:
            url = config.URLS['get_student'] + password
            result = httpService.get(url)
            if result:
                self.student = result.json()

        return self.student


if __name__ == '__main__':
    sm = StudentManager()
    x = sm.get_student("123456789")
    print(sm.get_student())
    print(sm.student)
    sm1 = StudentManager()
    print(sm1.student)
    print(sm1.get_student())
