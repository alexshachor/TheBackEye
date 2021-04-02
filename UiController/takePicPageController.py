from PIL import Image
from UiController import uiController
from Measurements import faceRecognition as fr
import config
import time


def check_recognition(path):
    if config.DEBUG:
        time.sleep(2)
        return True
    # TODO - check if image need to be change into frame.
    img = Image.open(path)
    return fr.FaceRecognition().run(img)


def successes():
    uiController.destructor()
