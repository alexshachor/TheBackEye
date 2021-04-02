from Measurements import abstractMeasurement as am


class FaceDetector(am.AbstractMeasurements):

    def __init__(self):
        am.AbstractMeasurements.__init__(self)

    def run(self, frame, q_results):
        try:

            am.AbstractMeasurements.run(self, frame)
            # ....
            # ...
            # EXAMPLE run
            result = {'face_detector': True}
            q_results.put(result)
        except:
            # write error to log file
            pass

    def __repr__(self):
        return 'FaceDetector'
