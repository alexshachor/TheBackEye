import config
from Services import httpService

student = None


class StudentManager:
    """
    This class manages the student details that come from remote.
    """

    @staticmethod
    def get_student(password=None):
        """
        Get specific student from remote
        :param password: the student's password
        :return: student details dictionary
        """
        global student
        if password:
            url = config.URLS['get_student'] + password
            result = httpService.get(url)
            if result:
                student = result.json()

        return student




if __name__ == '__main__':
    res = StudentManager.get_student("123456789")
    if res:
        print(StudentManager.get_student())
