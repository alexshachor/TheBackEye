import time


class LoginController:

    def __init__(self, name, id):
        self.name = name
        self.id = id

    @staticmethod
    def check_validation(obj, string):
       pass

    def has_pic(self):
        # TODO - send name and id to the server to check if we have already pic
        #  for this student if true return true else false (recognazie student by id and name).
        time.sleep(2)
        return False