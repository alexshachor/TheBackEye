import config
from Services import httpService


class LessonConfiguration():
    """
    This class manages the lesson configuration that come from remote.
    The configuration define a specific lesson's configuration.
    """
    def __init__(self, params):
        self.configuration = get_lesson_configuration(params)

    def get_configuration(self):
        """
        getter
        :return: configuration dictionary
        """
        return self.configuration


def get_lesson_configuration(params):
    """
    Get specific lesson configuration from remote
    :param params: params for the GET request (e.g: lesson_id)
    :return: configuration dictionary
    """
    url = config.URLS['lesson_configuration']
    result = httpService.get(url, params)
    return result
