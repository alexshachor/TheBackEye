import os
import psutil
import cv2

import config
from Services import httpService, loggerService


def get_program_status(program):
    def is_exe(file_path):
        return os.path.isfile(file_path) and os.access(file_path, os.X_OK)

    file_path, file_name = os.path.split(program)
    if file_path:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


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


def check_if_program_installed(program_name):
    """
    check if a given program is install on the computer.
    :param program_name: the name if the program
    :return: True if the program installed and False otherwise.
    """
    result = get_program_status(config.PREREQUISITE_PROGRAMS[program_name])
    loggerService.get_logger().info(f'is {program_name} installed = {result}')
    return {f'is_{program_name}_installed': result}


def check_if_process_is_running(process_name):
    """
    check if a given process is currently running.
    :param process_name: the name of the process.
    :return: True if the process is running and False otherwise.
    """
    result = process_name in (p.name() for p in psutil.process_iter())
    loggerService.get_logger().info(f'is {process_name} running = {result}')
    return {f'is_{process_name}_running': result}


def run_health_checks():
    """
    run all the health checks needed for the application to run
    :return: list of pairs which the key is the health check name and value True or False
    depending the health check result.
    """
    health_checks = []
    results = []

    # iterate over prerequisite installations and check if each one of them is installed
    for key, value in config.PREREQUISITE_INSTALLATIONS.items():
        results.append(check_if_program_installed(key))

    # iterate over prerequisite processes and check if each one of them is currently running
    for key, value in config.PREREQUISITE_PROCESSES.items():
        results.append(check_if_process_is_running(key))

    # iterate over the health checks, call it and append its result to results array
    for health_check in health_checks:
        results.append(health_check())

    return results
