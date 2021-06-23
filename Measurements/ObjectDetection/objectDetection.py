from Measurements import abstractMeasurement as am
from Services import loggerService as ls
import config
import os
import cv2


class ObjectDetection(am.AbstractMeasurement):

    def __init__(self):
        """
        initialize the parent class all paths & list of obj
        & list of the prohibited objects from the list of obj.
        """
        am.AbstractMeasurement.__init__(self)
        script_dir = os.path.dirname(__file__)
        self.class_file = os.path.join(script_dir, 'Files/objects.names')
        self.config_path = os.path.join(script_dir, 'Files/objects_config.pbtxt')
        self.weights_path = os.path.join(script_dir, 'Files/objects_weights.pb')
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
        """
        report if we detect prohibited obj. if yes
        update the dict_results to false else true.
        :param frame: frame to process
        :param dict_results: a dictionary which the result will be put there
        """
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
        """
        :return: the name of the measurement.
        """
        return 'ObjectDetection'

    def run_debug(self, objects, confidence, box):
        """
        if we in debug mode open a pop up window and show the obj
        the system detect with boxes painted over them.
        :param objects: the list of obj the system detect
        :param confidence: for each obj in what confidence the system have for
        identify him correctly.
        :param box: list of boxes
        """
        for obj, conf, b in zip(objects.flatten(), confidence.flatten(), box):
            cv2.rectangle(self.frame, b, color=(0, 145, 145), thickness=1)
            cv2.putText(self.frame, self.objects[obj - 1].upper(), (b[0] + 10, b[1] + 30),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
            cv2.putText(self.frame, str(round(conf * 100, 2)), (b[0], b[1] + 70),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 2)
        cv2.imshow("Output", self.frame)
        cv2.waitKey(0)

    def init_model(self):
        """
        this func will init model input size & scale
        """
        try:
            self.model = cv2.dnn_DetectionModel(self.weights_path, self.config_path)
            self.model.setInputSize(320, 320)
            self.model.setInputScale(1.0 / 100.5)
            self.model.setInputMean((100.5, 100.5, 100.5))
            self.model.setInputSwapRB(True)
        except ValueError as v:
            ls.get_logger().error(str(v))
        except Exception as e:
            ls.get_logger().error(f'failed to open files, due to: {str(e)}')


def for_tests_only():
    """
    A test func to this page only.
    """
    x = ObjectDetection()
    dict_res = {}
    image = cv2.imread('../../ImageProcessing/SavedImages/2.png')
    x.run(image, dict_res)
    print(dict_res[x.__repr__()])


if __name__ == '__main__':
    for_tests_only()
