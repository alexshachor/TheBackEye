import cv2
import numpy as np
from PIL import Image
import config


class FaceTraining:

    def __init__(self):
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.detector = cv2.CascadeClassifier('.\Models\haarcascade_frontalface_default.xml')
        self.image_paths = ['.\Images\\1.jpg', '.\Images\\2.jpg', '.\Images\\3.jpg',
                            '.\Images\\4.jpg', '.\Images\\5.jpg']
        print('[INFO] Training faces. It will take a few seconds.') if config.DEBUG else None
        self.faces, self.ids = self.__get_images_labels()
        self.__train()
        print('[INFO] faces trained. Exiting Program') if config.DEBUG else None

    # function to get the images and label data
    def __get_images_labels(self):
        pass

    def __train(self):
        pass


def for_tests_only():
    pass


if __name__ == "__main__":
    for_tests_only()
