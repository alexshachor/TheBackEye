import logging


# TODO: fetch default log name from config
def get_logger(log_name = './Logs/back_eye.log'):

    logging.basicConfig(filename=log_name,
                                filemode='a',
                                format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                                datefmt='%H:%M:%S',
                                level=logging.DEBUG)
    return logging.getLogger(log_name)

# Logs for example
# logger.debug('A debug message')
# logger.info('An info message')
# logger.warning('Something is not right.')
# logger.error('A Major error has happened.')
# logger.critical('Fatal error. Cannot continue')
