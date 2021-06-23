import config
from Services import httpService
import copy

lesson_from_server = None

class LessonConfiguration:
    """
    This class manages the lesson configuration that come from remote.
    The configuration define a specific lesson's configuration.
    """

    @staticmethod
    def get_lesson(lesson_code=None):
        """
        Get specific lesson from remote
        :param lesson_code: the lesson's password
        :return: lesson details dictionary
        """
        global student_from_server
        if lesson_code:
            url = config.URLS['get_lesson'] + lesson_code
            result = httpService.get(url)
            if result:
                lesson_from_server = result.json()

        return copy.deepcopy(lesson_from_server)


if __name__ == '__main__':
    lesson = LessonConfiguration.get_lesson("ABC")
    if lesson:
        print('got lesson from server: ', lesson)