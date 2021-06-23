from PIL import Image
from UiController import uiController
from Measurements.FaceRecognition import faceRecognition as fr
import cv2
import numpy
from Core import runMeasurements as rm
import config
import time


def check_recognition(path):
    """
    Check for student FaceRecognition.
    :param path: path to the snapshot image
    :return msg: True or false according to FaceRecognition result
    """
    # if config.DEBUG:
    #     time.sleep(2)
    #     return True
    # measurements = rm.RunMeasurements([fr.FaceRecognition()], None)
    # TODO - check if image need to be change into frame.
    img = Image.open(path)
    face_recognition_res = {}
    img = cv2.cvtColor(numpy.asarray(img), cv2.COLOR_RGB2BGR)
    fr.FaceRecognition().run(img, face_recognition_res)
    # face_recognition_res = measurements.run_measurement_processes(img)
    return face_recognition_res[fr.FaceRecognition().__repr__()]


def successes():
    """
    Go and destroy the Ui.
    """
    uiController.destructor()


if __name__ == '__main__':
    print(check_recognition(r"C:\Users\User\Downloads\1.jpg"))
