import logging

DEBUG = True
TIMEOUT = 5
CAM_SRC = 1

URLS = {
    'post_measures': 'http://bla/bla',
    'post_stacked_measures': 'http://test',
    'lesson_configuration': 'http://Configuration/blabla',
    'post_logs': 'http://logs/bla'
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
DESIRED_PROGRAM = {
    'EXPECTED_ON_TOP': 'zoom.exe',
    'HWND': 'Zoom Meeting'
}
APP = {
    'WIN_SIZE': '430x550+50+20',
    'TITLE': 'TheBackEye',
    'WIDTH': 430,
    'HEIGHT': 550,
    'FONT_OUTPUT': ("Ariel", 10),
    'FONT_MSG': ("Ariel", 10, "bold")
}
APPLICATION = None
USER_DATA = {
    'USERNAME': '',
    'ID': ''
}
HEAD_POSE = {
    'video_file': './video/result.avi',
    'snapshot_file': './checkpoint/snapshot/checkpoint.pth.tar',
    'range': {
        'yaw': (-10, 10),
        'pitch': (4, 20),
        'roll': (-30, 50)
    }
}
