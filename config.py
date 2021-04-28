import logging

DEBUG = True
TIMEOUT = 5
CAM_SRC = 1

URLS = {
    'post_measures': 'http://bla/bla',
    'post_stacked_measures': 'http://test',
    'lesson_configuration': 'http://Configuration/blabla',
    'post_logs':'http://logs/bla'
}

LOG_FILES = {
    'default': './Logs/back_eye.log'
}
LOG_OPTIONS = {
    'file_mode': 'a',
    'format': '%(asctime)s,%(msecs)d %(levelname)s %(message)s',
    'date_format': '%d/%m/%y %H:%M:%S',
    'level': logging.DEBUG
}

"""
what program should be on top & what are window name.
use: in onTop.py
"""
DESIRED_PROGRAM = {
    'EXPECTED_ON_TOP': 'zoom.exe',
    'HWND': 'Zoom Meeting'
}

"""
all the data about the app.
use: in uiController.py
"""
APP = {
    'WIN_SIZE': '430x550+50+20',
    'TITLE': 'TheBackEye',
    'WIDTH': 430,
    'HEIGHT': 550,
    'FONT_OUTPUT': ("Ariel", 10),
    'FONT_MSG': ("Ariel", 10, "bold")
}

"""
gui app object.
use: in uiController.py
"""
APPLICATION = None

"""
the name & id the student enter with to the app.
use: loginPage & probably in the warning system
"""
USER_DATA = {
    'USERNAME': '',
    'ID': ''
}

"""
what object we do not allow the student to mess with during lesson
we probably should receive this objects from the teacher.
use: in class ObjectDetector
"""
PROHIBITED_OBJECTS = ['CELL PHONE']

"""
teacher msgs for the student if the student fail in the
measurements.
use: in voice system
"""
TEACHER_MSGS = None
