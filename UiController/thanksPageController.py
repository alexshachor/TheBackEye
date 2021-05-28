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


def get_debug_time():
    """
    create a time object in debug mode.
    :return: combined: a datetime object
    """
    date = datetime.datetime.strptime('2021-05-28', "%Y-%m-%d")
    t = datetime.time(19, 00)
    combined = datetime.datetime.combine(date.date(), t)
    return combined


def for_tests_only():
    """
    this function is for tests only
    """
    hour, minute = get_time_remaining()
    print(hour, minute)


if __name__ == "__main__":
    for_tests_only()
