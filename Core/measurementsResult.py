import datetime

class MeasurementsResult:
    def __init__(self, measurements_result):
        self.result =  measurements_result
        self.time = datetime.datetime.now()
