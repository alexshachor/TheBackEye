import cv2

import config
from Services import httpService, loggerService


def check_is_alive():
    """
    check if the server is alive and respond.
    :return: pair of test kind and True or False if the test was success or failure.
    """
    is_alive = httpService.head(config.URLS['is_alive'])
    loggerService.get_logger().info(f'is alive = {is_alive}')
    return {'is_alive': is_alive}


def check_camera_source():
    """
    check if able to read from camera by the configured CAM_SRC, if was not able to read,
    try a range of numbers [0-10] and configure the new source if was success.
    :return: pair of test kind and True or False if the test was success or failure.
    """
    success_msg = 'read from camera source was success. source value = {cam_src}'
    failure_msg = 'read from camera source failed. source value = {cam_src}'
    res_key = 'camera_source'

    # at first, try to read camera by CAM_SRC value
    ret, frame = cv2.VideoCapture(config.CAM_SRC).read()
    if ret:
        loggerService.get_logger().info(success_msg.format(cam_src=config.CAM_SRC))
        return {res_key: True}
    # try each one of the values in range [0-10] until reading success
    for i in range(0, 11):
        ret, frame = cv2.VideoCapture(i).read()
        if ret:
            # set CAM_SRC to be i from now on
            config.CAM_SRC = i
            loggerService.get_logger().info(success_msg.format(cam_src=i))
            return {res_key: True}

    loggerService.get_logger().fatal(failure_msg.format(cam_src=config.CAM_SRC))
    return {res_key: False}


def run_health_checks():
    health_checks = []
