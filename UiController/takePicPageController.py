from PIL import Image
from UiController import uiController
from Measurements import faceRecognition as fr
from Core import runMeasurements as rm
import config
import time


def check_recognition(path):
    """
    Check for student FaceRecognition.
    :param path: path to the snapshot image
    :return msg: True or false according to FaceRecognition result
    """
    measurements = rm.RunMeasurements([fr.FaceRecognition()], None)
    if config.DEBUG:
        time.sleep(2)
        return True
    # TODO - check if image need to be change into frame.
    img = Image.open(path)
    face_recognition_res = measurements.run_measurement_processes(img)
    return face_recognition_res['FaceRecognition']


def successes():
    """
    Go and destroy the Ui.
    """
    uiController.destructor()
