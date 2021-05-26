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
        am.AbstractMeasurement.run(self, frame, dict_results)
        result = {repr(self): False}
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.get_faces(frame, gray)
            for (x, y, w, h) in faces:
                self.id, confidence = self.recognizer.predict(gray[y:y + h, x:x + w])
                # check if confidence is less them 100, zero is perfect confidence
                if confidence < 100:
                    if round(100 - confidence) >= self.threshold:
                        result[repr(self)] = True
                if config.DEBUG:
                    self.run_debug(frame, x, y, h, w, confidence)
            dict_results.update(result)
        except Exception as e:
            ls.get_logger().error(
                f'Failed in face recognition, due to: {str(e)}')

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
