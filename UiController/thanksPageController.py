import config
import datetime
import os
import psutil


def get_time_remaining():
    """
    this function get the time remaining for the lesson.
    :return: date_time_obj[0]: hours
    :return: date_time_obj[1]: minutes
    """
    # TODO: get the time remaining from lesson configuration & get the real late_time
    lesson_start_time = get_debug_time() if config.DEBUG else None
    late_time = 10 if config.DEBUG else None
    time_left = (lesson_start_time - datetime.datetime.now()).total_seconds() / 60
    if str(time_left)[0] == '-':
        return ('V', 'V') if late_time - (-1*time_left) > 0 else ('X', 'X')
    hours = int(int(str(time_left).split('.')[0]) / 60)
    minutes = int(time_left - hours * 60)
    return hours, minutes


def kill_program():
    """
    kill the program from a thread.
    """
    current_system_pid = os.getpid()
    this_sys = psutil.Process(current_system_pid)
    this_sys.terminate()


def get_debug_time():
    """
    create a time object in debug mode.
    :return: combined: a datetime object
    """
    date = datetime.datetime.strptime('2021-06-03', "%Y-%m-%d")
    # date = datetime.datetime.
    t = datetime.time(22, 45)
    combined = datetime.datetime.combine(date.date(), t)
    print(type(combined))
    return combined


def for_tests_only():
    """
    this function is for tests only
    """
    hour, minute = get_time_remaining()
    print(hour, minute)


if __name__ == "__main__":
    for_tests_only()
