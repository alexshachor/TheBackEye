from Measurements import abstractMeasurement as am
from Services import loggerService as ls
import config
import time
import cv2


class ObjectDetection(am.AbstractMeasurement):

    def __init__(self):
        pass

    def run(self, frame, dict_results):
        pass

    def __repr__(self):
        pass

    def run_debug(self, objects, confidence, box):
        pass

    def init_model(self):
        pass


def for_tests_only():
    pass


if __name__ == '__main__':
    for_tests_only()
