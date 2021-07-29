import datetime

from Core.lessonConfiguration import LessonConfiguration
from Core.studentManager import StudentManager
from Measurements import soundCheck, faceDetector, onTop
from Measurements.ObjectDetection import objectDetection as od
from Measurements.SleepDetector import sleepDetector as sd
from Measurements.HeadPose import headPose as hp
from Measurements.FaceRecognition import faceRecognition as fr


class MeasurementsResult:
    """
    This class holds the result and current time in order to know what time the measures were taken
    """

    def __init__(self, measurements_result):
        """
        initialize the class by setting the result and the current time.
        :param measurements_result: a dictionary which contains all the measurements result.
        """
        self.result = measurements_result
        self.time = datetime.datetime.now()

    def get_measurement_dto(self):
        """
        return measurements data and time as MeasurementDto as server format
        :return: MeasurementDto in format supported by the server
        """
        # return {
        #     "id": 0,
        #     "dateTime": self.time.isoformat() + 'Z',
        #     "headPose": self.result['HeadPose'],
        #     "faceRecognition": self.result['FaceRecognition'],
        #     "sleepDetector": self.result['SleepDetector'],
        #     "onTop": self.result['OnTop'],
        #     "faceDetector": self.result['FaceDetector'],
        #     "objectDetection": self.result['ObjectDetection'],
        #     "soundCheck": self.result['SoundCheck'],
        #     "lesson": {},
        #     "lessonId": LessonConfiguration.get_lesson()['id'],
        #     "person": {},
        #     "personId": StudentManager.get_student()['id']
        # }
        self.result['id'] = 0
        self.result['dateTime'] = self.time.isoformat() + 'Z'
        self.result['lessonId'] = LessonConfiguration.get_lesson()['id']
        self.result['personId'] = StudentManager.get_student()['id']
        self.result['lesson'] = None
        self.result['person'] = None
        return self.result
