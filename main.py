from Core.studentManager import StudentManager
from UiController import uiController
from Services.zoomService import ZoomService
from Core.lessonConfiguration import LessonConfiguration as lc
from Core.runMeasurements import RunMeasurements as rm
from Measurements import soundCheck, faceDetector, onTop
from Measurements.ObjectDetection import objectDetection as od
from Measurements.SleepDetector import sleepDetector as sd
from Measurements.HeadPose import headPose as hp
from Measurements.FaceRecognition import faceRecognition as fr

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print(StudentManager.get_student("jc?@jJQR>r"))
    # lesson = ")[(.O6cRNE\\"
    # print(lc.get_lesson(lesson))

    uiController.run()
    try:
        ZoomService(lc.get_lesson()['link']).join()
    except:
        pass

    measurements = [soundCheck.SoundCheck(), faceDetector.FaceDetector(), onTop.OnTop(),
                    sd.SleepDetector(), hp.HeadPose(), od.ObjectDetection(), fr.FaceRecognition()]
    rm(measurements, lc.get_lesson()).run()
    print('Closing application..')
