from Measurements import abstractMeasurement as am


class FaceDetector(am.AbstractMeasurements):

    def __init__(self):
        am.AbstractMeasurements.__init__(self)

    def run(self, frame):
        try:

            am.AbstractMeasurements.run(self, frame)
            # ....
            # ...
        except:
            # write error to log file
            pass

    def __repr__(self):
        return 'FaceDetector'
