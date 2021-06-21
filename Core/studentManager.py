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

    @staticmethod
    def update_student():
        """
        Get specific student from remote
        :param password: the student's password
        :return: student details dictionary
        """
        global student
        if student:
            url = config.URLS['put_student']
            result = httpService.put(url, student)
            if result:
                student = result.json()

        return student


if __name__ == '__main__':
    res_get = StudentManager.get_student("123456789")
    if res_get:
        print(StudentManager.get_student())
        res_get['person']['firstName'] = 'Moshe'
        res_put = StudentManager.update_student()
        if res_put:
            print(StudentManager.get_student())