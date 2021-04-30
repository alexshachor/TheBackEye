import config
from Services import httpService

def check_is_alive():
    """

    :return:
    """
    is_alive = httpService.head(config.URLS['is_alive'])
    return {'is_alive': is_alive}


def run_health_checks():
    health_checks = []
