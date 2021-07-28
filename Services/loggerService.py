import logging
import datetime

import config
from Services import httpService
from Core.studentManager import StudentManager


def get_logger(log_name=config.LOG_FILES['default']):
    """
    get logger by log name and write by variety of levels: [debug, info, warning, error, critical]
    :param log_name: the name of the log file
    :return: void
    """

    # Log's levels for example:
    # logger.debug('A debug message')
    # logger.info('An info message')
    # logger.warning('Something is not right.')
    # logger.error('A Major error has happened.')
    # logger.critical('Fatal error. Cannot continue')

    logging.basicConfig(filename=log_name,
                        filemode=config.LOG_OPTIONS['file_mode'],
                        format=config.LOG_OPTIONS['format'],
                        datefmt=config.LOG_OPTIONS['date_format'],
                        level=config.LOG_OPTIONS['level'])
    return logging.getLogger(log_name)


def send_log_reports(log_name=config.LOG_FILES['default']):
    """
    send the given log file to the server.
    :param log_name: the name of log file to send.
    :return: True if the logs successfully sent and False otherwise.
    """
    with open(log_name) as f:
        log_lines = f.readlines()
    log_dto = get_log_dto(log_lines)
    return httpService.post(config.URLS['post_logs'], log_dto)


def get_log_dto(log_lines):
    """
    get a log dto object contains log details and data
    :param log_lines: the log data from file
    :return: log_dto object
    """
    return {
        'id': 0,
        'creationDate': datetime.datetime.now().isoformat() + 'Z',
        'data': str(log_lines),
        'person': {},
        'personId': StudentManager.get_student()['id']
    }


if __name__ == '__main__':
    student = StudentManager.get_student("123")
    if student:
        res = send_log_reports()
        if res:
            print('result: ', res.text)
