import cv2
from Measurements import abstractMeasurement as am
from Services import loggerService as ls
import config


class FaceRecognition(am.AbstractMeasurement):

    def __init__(self):
        am.AbstractMeasurement.__init__(self)
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read('.\Models\\trainer.yml')
        self.cascade_path = '.\Models\haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(self.cascade_path)
        self.threshold = 45
        self.id = 0
        # names related to ids - example, Shalom: id=3
        self.names = ['None', config.USER_DATA['USERNAME'], 'Alex', 'Shalom', 'L', 'Z', 'W']

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
