import logging
from datetime import datetime

import config
from Services import httpService, datetimeService



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


def send_log_reports(person_id, log_name=config.LOG_FILES['default']):
    """
    send the given log file to the server.
    :param person_id: the id of the student
    :param log_name: the name of log file to send.
    :return: True if the logs successfully sent and False otherwise.
    """
    with open(log_name) as f:
        log_lines = f.readlines()
    log_dto = get_log_dto(log_lines, person_id)
    return httpService.post(config.URLS['post_logs'], log_dto)


def get_log_dto(log_lines, person_id):
    """
    get a log dto object contains log details and data
    :param log_lines: the log data from file
    :param person_id: the id of the student
    :return: log_dto object
    """
    return {
        'id': 0,
        'creationDate': datetimeService.convert_datetime_to_iso(datetime.now()),
        'data': str(log_lines),
        'person': None,
        'personId': person_id
    }


if __name__ == '__main__':

    res = send_log_reports("123")
    if res:
        print('result: ', res.text)
