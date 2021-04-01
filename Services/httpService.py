import requests
from Services import loggerService


def get(url, params):

    try:
        if not url:
            raise ValueError(f'cannot get, url is missing')
        r = requests.get(url, params)
        r.raise_for_status()
        return r.json()
    except ValueError as e:
        loggerService.get_logger().error(str(e))
        return None
    except Exception as e:
        loggerService.get_logger().error(
            f'get call to url: {url} has failed with status: {r.status_code}, due to: {str(e)}')
        return None


def post(url, data):

    try:
        if not data or not url:
            raise ValueError(f'cannot post, one of the params is missing. url: {url}, data: {data}')
        r = requests.post(url, data)
        r.raise_for_status()
        return r.ok
    except ValueError as e:
        loggerService.get_logger().error(str(e))
        return False
    except Exception as e:
        loggerService.get_logger().error(
            f'post call to url: {url}, data: {data} has failed with status: {r.status_code}, due to: {str(e)}')
        return False
