import config
from Services import httpService


class LessonConfiguration():
    def __init__(self, params):
        self.configuration = get_lesson_configuration(params)

    def get_configuration(self):
        return self.configuration


def get_lesson_configuration(params):
    url = config.URLS['lesson_configuration']
    result = httpService.get(url, params)
    return result
