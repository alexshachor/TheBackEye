import time
import config


class LoginController:
    """
    This class is responsible for the page login.
    """
    def __init__(self, name, id):
        """
        Init variables.
        :param name: the student name
        :param id: the student id
        """
        self.name = name
        self.id = id

    @staticmethod
    def check_validation(obj, string):
        """
        Check validation of student id or name.
        :param obj: name or id
        :param string: what to check
        """
        if len(string) == 0:
            return obj + ' Can not be empty.'
        if obj == 'Name':
            if string.replace(' ', '').isalpha():
                if len(string.split(' ')) == 1:
                    return 'Please enter a full name with space.'
                return 'OK' if (' ' in string and string.split(' ')[1] != '') else 'Please enter a full name.'
            return 'Name should not contain any numbers'
        else:
            if len(string) == 9:
                return 'OK' if string.isnumeric() else 'ID should not contain any letters.'
            return 'ID need to be at len 9.'

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
