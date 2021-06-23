import time
import config
import os


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

    def chech_student_data_in_server(self):
        # TODO: send the class code to the server [to get lesson by class code] and if it returns
        # a lesson store it in the static class and return OK else return their is no class with this class code.
        return 'OK' if config.DEBUG else None

    @staticmethod
    def has_pic_and_email():
        """
        Check if we already have email and pics for this student.
        """
        if config.DEBUG:
            time.sleep(2)
            return 'ToValidation'
        # TODO - check in the static class if the student has mail already if no return ToValidation.
        # TODO - send student id to the server to check if we have already pic if no return ToUpload
        # if yes store them in the face recognition images folder and train the model on them and return
        #  ToSnapshot.

        # check if the student already has images
        files = os.listdir('Measurements/FaceRecognition/Images')
        if files == ['1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg']:
            return 'ToSnapshot'
