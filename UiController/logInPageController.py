import time
import config


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

    def check_validation(self):
        """
        Check validation of student password & class_code.
        """
        if len(self.class_code) == 0:
            return 'Class Code cannot be empty.'
        if len(self.password) == 0:
            return 'Password Code cannot be empty.'
        if not all(ord(c) < 128 for c in self.class_code):
            return 'Class Code not in ascii.'
        if not all(ord(c) < 128 for c in self.password):
            return 'Password not in ascii.'

    @staticmethod
    def check_class_code(class_code):
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
