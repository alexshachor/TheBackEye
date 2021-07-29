import datetime

import cv2
from time import sleep
import config
from Core.measurementsResult import MeasurementsResult
from Services import loggerService
from Services.runMeasurementsService import MeasurementsService
import multiprocessing as mp


class RunMeasurements:
    """*************************************** Description of the Class - RunMeasurements:
        Gaol: This class is responsible for running all measurements and sending
        the results data to the server.
    ***********************************************************************************"""

    def __init__(self, measurements, lesson_configuration):
        """********************************* Description of the Function - __init__:
                Gaol: The constructor function.
                Parameters: measurements - List of objects [each object is a measure
                that needs to be executed and get its results].
                lesson_configuration - lesson configuration dictionary which hold the
                configuration of a specific lesson such as lesson duration and breaks.
            *************************************************************************"""

        self.measurements = measurements
        self.lesson = {
            'start': lesson_configuration['startTime'],
            'end': lesson_configuration['endTime'],
            'breaks': [(lesson_configuration['breakStart'], lesson_configuration['breakEnd'])]
            if lesson_configuration['breakStart'] is not None else []
        }

    def run(self):
        """************************************** Description of the Function - run:
              Gaol: Streaming from the user's camera at regular intervals, for the
              captured frame all the objects of the measurement are activated - the
              results are sent to the server.
              Parameters: self.
          *************************************************************************"""

        measurements_service = MeasurementsService()

        try:
            capture_device = cv2.VideoCapture(config.CAM_SRC, cv2.CAP_DSHOW)
            # assign current_break to be None if there are no breaks. otherwise, assign first break
            current_break = None if len(self.lesson['breaks']) == 0 else self.lesson['breaks'].pop(0)
            current_time = datetime.datetime.now()

            # if lesson start time is yet to be started, sleep for the time between
            if current_time < self.lesson['start']:
                sleep((self.lesson['start'] - current_time).seconds)

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
                result = self.run_measurement_processes(frame)
                measurements_service.post_measurements(MeasurementsResult(result))

                sleep(config.TIMEOUT)
                current_time = datetime.datetime.now()

            capture_device.release()
            self.finish_lesson()
        except Exception as e:
            loggerService.get_logger().error(f'an error occurred: {str(e)}')
            return

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
            process = mp.Process(target=job, args=(frame, dict_results))
            process.start()
            processes.append(process)

        for process in processes:
            # TODO: do we need to use timeout (if one of the processes is taking too long time to finish)?
            # TODO: what we do in case of one of the processes has not finished yet?
            process.join()
            process.close()

        return dict_results

    def finish_lesson(self):
        """
        all the logic concerning finishing lesson will be activated from here.
        :return: void
        """
        cv2.destroyAllWindows()
        loggerService.get_logger().info('lesson ended')
        loggerService.send_log_reports()
