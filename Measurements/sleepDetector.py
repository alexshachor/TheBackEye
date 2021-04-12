from Measurements import abstractMeasurement as am
from Services import loggerService as ls
import config
import cv2


class SleepDetector(am.AbstractMeasurement):

    def __init__(self):
        am.AbstractMeasurement.__init__(self)
        self.path = '../MeasurementsFilsAndModels/haarcascade_eye_tree_eyeglasses.xml'
        try:
            self.eye_cascade = cv2.CascadeClassifier(self.path)
        except FileNotFoundError as f:
            ls.get_logger().error(str(f))
        except Exception as e:
            ls.get_logger().error(f'failed to open files, due to: {str(e)}')

    def run(self, frame, dict_results):
        am.AbstractMeasurement.run(self, frame, dict_results)
        eyes = None
        result = {repr(self): False}
        try:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            eyes = self.eye_cascade.detectMultiScale(frame, scaleFactor=1.1,
                                                     minNeighbors=1, minSize=(1, 1))
        except Exception as e:
            ls.get_logger().error(
                f'Failed to identify the eyes, due to: {str(e)}')
        if eyes is None:
            ls.get_logger().error(
                f'Failed to identify the eyes, due to: There are no eyes in the frame\n'
                f'Possible reasons: wearing glasses, problematic lighting.')
            dict_results.update(result)
            return
        result[repr(self)] = True if len(eyes) != 0 else False

    def __repr__(self):
        return 'SleepDetector'


