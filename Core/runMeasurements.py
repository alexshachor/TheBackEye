import cv2
from time import sleep
import config
from Services import loggerService
from Services.runMeasurementsService import MeasurementsService


class RunMeasurements:

    def __init__(self, measurements, lesson_configuration):
        # [fd.FaceDetector(),hp(),ot(),sd()]
        self.measurements = measurements
        self.configuration = lesson_configuration

    def run(self):
        measurements_service = MeasurementsService()

        try:
            capture_device = cv2.VideoCapture(config.CAM_SRC, cv2.CAP_DSHOW)
            # TODO: get the lesson time from self.configuration['lesson_time'] and change the while accordingly
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
