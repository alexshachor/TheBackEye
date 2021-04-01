import requests
from Services import loggerService


def get(url, params):
    """
    get response from server by the given url and its params
    :param url: get the data from the url
    :param params: params needed for the request
    :return: the response in json format if succeed and None otherwise
    """
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
    """
    post the given data to the given url
    :param url: post the data to this url
    :param data: data to send the server
    :return: True if succeed and False otherwise
    """
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
