import os
from Core.studentManager import StudentManager as sm
from Core.lessonConfiguration import LessonConfiguration as lc


class LoginController:
    """
    This class is responsible for the page login.
    """
    def __init__(self, password, class_code):
        """
        Init variables.
        :param name: the student name
        :param id: the student id
        """
        self.password = password
        self.class_code = class_code
        self.msg = {'Class Code': '', 'Password': ''}

    def check_validation(self):
        """
        Check validation of student password & class_code.
        """
        if len(self.class_code) == 0:
            self.msg['Class Code'] += 'Class Code cannot be empty.\n'
        if len(self.password) == 0:
            self.msg['Password'] += 'Password cannot be empty.\n'
        if not all(ord(c) < 128 for c in self.class_code):
            self.msg['Class Code'] += 'Class Code not in ascii.\n'
        if not all(ord(c) < 128 for c in self.password):
            self.msg['Password'] += 'Password not in ascii.\n'
        return self.msg

    def check_student_data_in_server(self):
        msg = {'Class Code': '', 'Password': ''}
        password_res = sm.get_student(self.password)
        if password_res is None:
            msg['Password'] = 'This Password dedent exists in our system, please try again.'
        code_res = lc.get_lesson(self.class_code)
        if code_res is None:
            msg['Class Code'] = 'This Class Code dedent exists in our system, please try again.'
        return msg

    @staticmethod
    def has_pic_and_email():
        """
        Check if we already have email and pics for this student.
        """
        res = sm.get_student()
        if res['email'] == '':
            return 'ToValidation'
        else:
            # check if the student already has images
            files = os.listdir('Measurements/FaceRecognition/Images')
            if files == ['1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg']:
                return 'ToSnapshot'
            else:
                return 'ToUpload'
