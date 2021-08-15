import datetime
import threading

import cv2
from time import sleep
import config
from Core.measurementsResult import MeasurementsResult
from Services import loggerService, datetimeService
from Services.runMeasurementsService import MeasurementsService
import multiprocessing as mp
from Core.studentManager import StudentManager
from ImageProcessing import superResolution as sr
from WarningSystem.runSystem import RunSystem
from Core.lessonConfiguration import LessonConfiguration as lc
from Measurements import soundCheck, faceDetector, onTop
from Measurements.ObjectDetection import objectDetection as od
from Measurements.SleepDetector import sleepDetector as sd
from Measurements.HeadPose import headPose as hp
from Measurements.FaceRecognition import faceRecognition as fr


class RunMeasurements:
    """
    This class is responsible for running all measurements and sending the results data to the server.
    """

    def __init__(self, measurements, lesson_configuration):
        """
        The constructor function
        :param measurements: List of objects [each object is a measure
                that needs to be executed and get its results]
        :param lesson_configuration: lesson configuration dictionary which hold the
                configuration of a specific lesson such as lesson duration and breaks.
        """
        self.measurements_interval = {'SoundCheck': [], 'OnTop': [], 'FaceDetector': [],
                                      'SleepDetector': [], 'ObjectDetection': [],
                                      'HeadPose': [], 'FaceRecognition':[]}
        self.measurements = measurements
        self.lesson = {
            'start': datetimeService.convert_iso_format_to_datetime(lesson_configuration['startTime']),
            'end': datetimeService.convert_iso_format_to_datetime(lesson_configuration['endTime']),
            'breaks': [(datetimeService.convert_iso_format_to_datetime(lesson_configuration['breakStart']),
                        datetimeService.convert_iso_format_to_datetime(lesson_configuration['breakEnd']))]
            if datetimeService.convert_iso_format_to_datetime(
                lesson_configuration['breakStart']) is not datetime.MINYEAR else []
        }

    def run(self):
        """
        Streaming from the user's camera at regular intervals, for the
              captured frame all the objects of the measurement are activated - the
              results are sent to the server
        :return: void
        """
        measurements_service = MeasurementsService()
        try:
            # assign current_break to be None if there are no breaks. otherwise, assign first break
            current_break = None if len(self.lesson['breaks']) == 0 else self.lesson['breaks'].pop(0)
            current_time = alert_counter = interval_counter = datetime.datetime.now()

            # if lesson start time is yet to be started, sleep for the time between
            if current_time < self.lesson['start']:
                sleep((self.lesson['start'] - current_time).seconds)

            # turn on computer camera
            capture_device = cv2.VideoCapture(config.CAM_SRC, cv2.CAP_DSHOW)
            current_time = datetime.datetime.now()
            loggerService.get_logger().info('lesson started')

            # if current time is still in range of lesson time
            while self.lesson['start'] <= current_time < self.lesson['end']:
                # if it's time to break then sleep for the break duration
                if current_break is not None and current_break[0] <= current_time < current_break[1]:
                    sleep((current_break[1] - datetime.datetime.now()).seconds + 1)
                    current_break = None if len(self.lesson['breaks']) == 0 else self.lesson['breaks'].pop(0)

                ret, frame = capture_device.read()
                if not ret:
                    loggerService.get_logger().fatal(f'cannot read from camera source. source value = {config.CAM_SRC}')
                    continue
                frame = sr.SuperResolution(frame, 0).get_image()

                measurements_results = self.run_measurement_threads(frame)

                # measurements_results = {}
                # for job in self.measurements:
                #     job.run(frame, measurements_results)
                if config.DEBUG:
                    print(measurements_results)

                self.update_measurements_interval(measurements_results)
                if (datetime.datetime.now() - alert_counter).seconds > config.ALERT_SYSTEM['interval_seconds']:
                    # RunSystem(measurements_results)
                    self.update_measurements_by_interval(measurements_results)
                    thread = threading.Thread(target=RunSystem, args=(measurements_results,))
                    thread.start()
                    alert_counter = datetime.datetime.now()

                # TODO: uncomment the 2 lines inside the if statement acorrding to the logic in the teacher side.
                if (datetime.datetime.now() - interval_counter).seconds > config.MEASUREMENT_INTERVAL['interval_seconds']:
                    # self.update_measurements_by_interval()
                    self.reset_measurements_interval()
                    # measurements_service.post_measurements(MeasurementsResult(measurements_results))

                measurements_service.post_measurements(MeasurementsResult(measurements_results))

                sleep(config.TIMEOUT)
                current_time = datetime.datetime.now()

            capture_device.release()
            self.finish_lesson()
        except Exception as e:
            loggerService.get_logger().error(f'an error occurred: {str(e)}')
            return

    def update_measurements_by_interval(self, measurements_results):
        for key, val in self.measurements_interval.items():
            if key in ['FaceDetector', 'SleepDetector', 'HeadPose', 'FaceRecognition']:
                measurements_results[key] = True if True in val else False
            else:
                measurements_results[key] = False if False in val else True

    def reset_measurements_interval(self):
        for val in self.measurements_interval.values():
            val.clear()

    def update_measurements_interval(self, measurements_results):
        for key, val in measurements_results.items():
            self.measurements_interval[key].append(val)

    def run_measurement_processes(self, frame):
        """
        run all measurements in a parallel, wait them all to finish, and return their result.
        :param frame: frame to measure.
        :return: results - dictionary of the results [key = measurement name, value = measurement result]
        """
        dict_results = mp.Manager().dict()
        # assign all processes and start each one of them
        processes = []
        for job in self.measurements:
            process = mp.Process(target=job.run, args=(frame, dict_results,))
            process.start()
            processes.append(process)

        for process in processes:
            process.join()
            process.close()

        return dict_results

    def run_measurement_threads(self, frame):
        """
        run all measurements each one in different thread, wait them all to finish, and return their result.
        :param frame: frame to measure.
        :return: results - dictionary of the results [key = measurement name, value = measurement result]
        """
        dict_results = mp.Manager().dict()
        # assign all threads and start each one of them
        threads = []
        for job in self.measurements:
            thread = threading.Thread(target=job.run, args=(frame, dict_results,))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()

        return dict_results

    def finish_lesson(self):
        """
        all the logic concerning finishing lesson will be activated from here.
        :return: void
        """
        cv2.destroyAllWindows()
        loggerService.get_logger().info('lesson ended')
        loggerService.send_log_reports(StudentManager.get_student())


if __name__ == '__main__':
    StudentManager.get_student("999")
    lc.get_lesson("999")
    measurements = [soundCheck.SoundCheck(), faceDetector.FaceDetector(), onTop.OnTop(),
                    sd.SleepDetector(), hp.HeadPose(), od.ObjectDetection(), fr.FaceRecognition()]
    RunMeasurements(measurements, lc.get_lesson()).run()
