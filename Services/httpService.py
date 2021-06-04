import base64
import json

import requests
from Services import loggerService


def get(url, params = None):
    """
    get response from server by the given url and its params
    :param url: get the data from the url
    :param params: params needed for the request
    :return: the response in json format if succeed and None otherwise
    """
    try:
        if not url:
            raise ValueError(f'cannot get, url is missing')
        response = requests.get(url, params)
        response.raise_for_status()
        # data = response.json()
        return response
    except ValueError as e:
        loggerService.get_logger().error(str(e))
        return None
    except requests.exceptions.RequestException:
        loggerService.get_logger().error(str(response.text))
        return None
    except Exception as e:
        loggerService.get_logger().error(
            f'get call to url: {url} has failed with status: {response.status_code}, due to: {str(e)}')
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
        response = requests.post(url, data)
        response.raise_for_status()
        return response.ok
    except ValueError as e:
        loggerService.get_logger().error(str(e))
        return False
    except requests.exceptions.RequestException:
        loggerService.get_logger().error(str(response.text))
        return False
    except Exception as e:
        loggerService.get_logger().error(
            f'post call to url: {url}, data: {data} has failed with status: {response.status_code}, due to: {str(e)}')
        return False


def post_image_data(url, data, image_file):
    """
    post the given data to the given url
    :param url: post the data to this url
    :param data: data to send the server
    :param image_file: image to send along with the data
    :return: True if succeed and False otherwise
    """
    try:
        if not data or not url or not image_file:
            raise ValueError(f'cannot post, one of the params is missing.'
                             f' url: {url}, data: {data}, image: {image_file}')

        with open(image_file, "rb") as f:
            im_bytes = f.read()
        im_b64 = base64.b64encode(im_bytes).decode("utf8")

        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

        payload = json.dumps({"image": im_b64, 'data': data})
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()
        return response.ok
    except ValueError as e:
        loggerService.get_logger().error(str(e))
        return False
    except requests.exceptions.RequestException:
        loggerService.get_logger().error(str(response.text))
        return False
    except Exception as e:
        loggerService.get_logger().error(
            f'post call to url: {url}, data: {data} has failed, due to: {str(e)}')
        return False


def head(url):
    """
    check if server is alive using HEAD call to the given url
    :param url: head call to the given url
    :return: True if server respond and False otherwise.
    """
    try:
        if not url:
            raise ValueError(f'cannot make head call, url is missing')
        response = requests.head(url)
        response.raise_for_status()
        return True if response.ok else False
    except ValueError as e:
        loggerService.get_logger().error(str(e))
        return False
    except requests.exceptions.RequestException as e:
        loggerService.get_logger().error(str(e))
        return False
    except Exception as e:
        loggerService.get_logger().error(
            f'head call to url: {url} has failed with status: {response.status_code}, due to: {str(e)}')
        return False

