from Measurements import abstractMeasurement as am
from Services import loggerService as ls
import config
import time
import cv2


class ObjectDetection(am.AbstractMeasurement):

    def __init__(self):
        am.AbstractMeasurement.__init__(self)
        self.class_file = '../MeasurementsFilsAndModels/objects.names'
        self.config_path = '../MeasurementsFilsAndModels/objects_config.pbtxt'
        self.weights_path = '../MeasurementsFilsAndModels/objects_weights.pb'
        self.prohibited_objects = config.PROHIBITED_OBJECTS
        self.model = None
        # Threshold to detect object
        self.threshold = 0.45
        self.init_model()
        try:
            self.objects = [line.strip() for line in open(self.class_file, 'rt')]
        except ValueError as v:
            ls.get_logger().error(str(v))
        except Exception as e:
            ls.get_logger().error(f'failed to open files, due to: {str(e)}')

    def run(self, frame, dict_results):
        am.AbstractMeasurement.run(self, frame, dict_results)
        result = {repr(self): False}
        try:
            objects, confidence, box = self.model.detect(frame, confThreshold=self.threshold)
            # Check for prohibited objects.
            for obj in objects.flatten():
                if self.objects[obj - 1].upper() in self.prohibited_objects:
                    dict_results.update(result)
                    break
            result[repr(self)] = True
            dict_results.update(result)
            if config.DEBUG:
                self.run_debug(objects, confidence, box)
        except Exception as e:
            ls.get_logger().error(
                f'Failed to detect objects, due to: {str(e)}')

    def __repr__(self):
        return 'ObjectDetection'

    def run_debug(self, objects, confidence, box):
        pass

    def init_model(self):
        pass


def for_tests_only():
    pass


if __name__ == '__main__':
    for_tests_only()
