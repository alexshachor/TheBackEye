import datetime


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
