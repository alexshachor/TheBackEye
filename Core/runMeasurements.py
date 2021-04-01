import cv2
from time import sleep
import config
from Services import loggerService
from Services.runMeasurementsService import MeasurementsService


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
                    continue
                result = {}
                for measure in self.measurements:
                    # TODO: run each algorithm in thread, then wait for their result using join
                    result[str(measure)] = measure.run(frame)
                measurements_service.post_measurements(result)
                # TODO: do we need these lines?
                # if cv2.waitKey(1) & 0xFF == ord('q'):
                #     break

                sleep(config.TIMEOUT)

            capture_device.release()
            cv2.destroyAllWindows()
        except Exception as e:
            loggerService.get_logger().error(f'error occurred: {str(e)}')
            return
