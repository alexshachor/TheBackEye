import config
import datetime


def get_time_remaining():
    """
    this function get the time remaining for the lesson.
    :return: date_time_obj[0]: hours
    :return: date_time_obj[1]: minutes
    """
    # TODO: get the time remaining from lesson configuration
    lesson_start_time = get_debug_time() if config.DEBUG else None
    time_left = lesson_start_time - datetime.datetime.now()
    print(time_left)
    if str(time_left)[0] == '-':
        return 'X', 'X'
    date_time_obj = str(time_left).split(':')
    return date_time_obj[0], date_time_obj[1]