import cv2
import config
from Measurements import abstractMeasurement as am
from Services import loggerService
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh


class HeadPose(am.AbstractMeasurements):

    def __init__(self):
        """
        initialize the parent class.
        """
        am.AbstractMeasurements.__init__(self)

    def run(self, frame, dict_results):
        """
        run the face detector algorithm on the given frame
        :param frame: frame to process.
        :param dict_results: a dictionary which the result will be put there
        :return: pair of key = 'face_detection', value = True if there is face and False otherwise.
            """
        run_result = {repr(self): False}
        try:
           

            # if results.multi_face_landmarks:
            #     # face has been detected
            #     run_result[repr(self)] = True
            #
            #     # if config.DEBUG:
            #     #     self.draw_annonations(image, results)
            dict_results.update(run_result)

        except Exception as e:
            # write error to log file
            loggerService.get_logger().error(str(e))

    def __repr__(self):
        return 'HeadPose'
