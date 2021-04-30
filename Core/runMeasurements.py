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

        # [fd.FaceDetector(),hp(),ot(),sd()]
        self.measurements = measurements
        self.configuration = lesson_configuration

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
            # TODO: get the lesson time from self.configuration['duration'] and change the while accordingly
            # TODO: add support for a break in the middle of the lesson
            while True:
                ret, frame = capture_device.read()
                if not ret:
                    loggerService.get_logger().fatal(f'cannot read from camera source. source value = {config.CAM_SRC}')
                    continue
                result = self.run_measurement_processes(frame)
                measurements_service.post_measurements(MeasurementsResult(result))
                if config.DEBUG & cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                sleep(config.TIMEOUT)

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
        loggerService.send_log_reports()
