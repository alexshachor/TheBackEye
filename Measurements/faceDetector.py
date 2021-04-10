import cv2
import config
from Measurements import abstractMeasurement as am
from Services import loggerService
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh


class FaceDetector(am.AbstractMeasurements):

    def __init__(self):
        """
        initialize the parent class and the face_mesh model.
        """
        am.AbstractMeasurements.__init__(self)
        self.face_mesh = mp_face_mesh.FaceMesh(
            min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

    def run(self, frame, q_results):
        """
        run the face detector algorithm on the given frame
        :param frame: frame to process.
        :return: pair of key = 'face_detection', value = True if there is face and False otherwise.
            """
        run_result = {repr(self): False}
        try:
            # flip the image in order to represent a true self of the person not mirror of it
            # and convert its colors.
            image = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
            # make it read only image in order to improve the performance
            image.flags.writeable = False
            # process it by face mesh model
            results = self.face_mesh.process(image)

            if results.multi_face_landmarks:
                # face has been detected
                run_result[repr(self)] = True
                # show face net on image
                if config.DEBUG:
                    self.draw_annonations(image, results)
            q_results.put(run_result)
        except Exception as e:
            self.face_mesh.close()
            # write error to log file
            loggerService.get_logger().error(str(e))

    def __repr__(self):
        return 'Face Detector'

    def draw_annotations(self, image, results):

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        for face_landmarks in results.multi_face_landmarks:
            # draw face landmark net
            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACE_CONNECTIONS,
                landmark_drawing_spec=self.drawing_spec,
                connection_drawing_spec=self.drawing_spec)
            cv2.imshow('MediaPipe FaceMesh', image)
