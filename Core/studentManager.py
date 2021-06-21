import config
from Services import httpService
import copy

student_from_server = None


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
        global student_from_server
        if password:
            url = config.URLS['get_student'] + password
            result = httpService.get(url)
            if result:
                student_from_server = result.json()

        return copy.deepcopy(student_from_server)

    @staticmethod
    def update_student(student_updated):
        """
        Get specific student from remote
        :param student: student to update
        :return: student details dictionary
        """
        global student_from_server
        if student_updated:
            url = config.URLS['put_student']
            result = httpService.put(url, student_updated)
            if result:
                student_from_server = result.json()

        return copy.deepcopy(student_from_server)


if __name__ == '__main__':
    student = StudentManager.get_student("123456789")
    if student:
        print('got student from server: ', student)
        # change something in student details
        student['person']['firstName'] = student['person']['firstName'] + 'DDD'
        print('got student after update: ', StudentManager.update_student(student))
        print('get from server after update: ', StudentManager.get_student("123456789"))
