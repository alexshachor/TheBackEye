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
                if not string.split(' ')[1]:
                    return 'Please enter a full name.'
                return 'OK' if ' ' in string else 'Please enter a full name with space.'
            return 'Name should not contain any numbers'
        else:
            if len(string) == 9:
                return 'OK' if string.isnumeric() else 'ID should not contain any letters.'
            return 'ID need to be at len 9.'

    @staticmethod
    def has_pic():
        if config.DEBUG:
            time.sleep(2)
            return False
        # TODO - send name and id to the server to check if we have already pic
        #  for this student if true return true else false (recognazie student by id and name).
