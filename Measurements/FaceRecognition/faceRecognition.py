import cv2
from Measurements import abstractMeasurement as am
from Services import loggerService as ls
import config


class FaceRecognition(am.AbstractMeasurement):

    def __init__(self):
        pass

    def run(self, frame, dict_results):
        pass

    def __repr__(self):
        """
        :return: the name of the measurement.
        """
        return 'FaceRecognition'

    def get_faces(self, frame, gray):
        pass

    def run_debug(self, img, x, y, h, w, confidence):
        pass


def for_tests_only():
    pass


if __name__ == "__main__":
    for_tests_only()