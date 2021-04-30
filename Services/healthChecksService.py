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
    success_msg = 'read from camera source was success. source value = {cam_src}'
    failure_msg = 'read from camera source failed. source value = {cam_src}'
    res_key = 'camera_source'

    capture_device = cv2.VideoCapture(config.CAM_SRC)
    ret, frame = capture_device.read()
    if ret:
        loggerService.get_logger().info(success_msg.format(cam_src=config.CAM_SRC))
        return {res_key: True}

    for i in range(0, 11):
        ret, frame = cv2.VideoCapture(i).read()
        if ret:
            config.CAM_SRC = i
            loggerService.get_logger().info(success_msg.format(cam_src=i))
            return {res_key: True}

    loggerService.get_logger().fatal(failure_msg.format(cam_src=config.CAM_SRC))
    return {res_key: False}


def run_health_checks():
    health_checks = []
