import logging
import config


def get_logger(log_name=config.LOG_FILES['default']):
    """
    get logger by log name and write by variety of levels: [debug, info, warning, error, critical]
    :param log_name: the name of the log file
    :return: void
    """
    logging.basicConfig(filename=log_name,
                        filemode=config.LOG_OPTIONS['file_mode'],
                        format=config.LOG_OPTIONS['format'],
                        datefmt=config.LOG_OPTIONS['date_format'],
                        level=config.LOG_OPTIONS['level'])
    return logging.getLogger(log_name)

# Logs for example
# logger.debug('A debug message')
# logger.info('An info message')
# logger.warning('Something is not right.')
# logger.error('A Major error has happened.')
# logger.critical('Fatal error. Cannot continue')
