import config
from Services import httpService


class MeasurementsService:
    def __init__(self):
        self.measurements_stack = []

    def post_measurements(self, measurements):
        has_success = httpService.post(config.URLS['post_measures'], measurements)
        if has_success:
            if len(self.measurements_stack) > 0:
                has_success = httpService.post(config.URLS['post_stacked_measures'], self.measurements_stack)
                if has_success:
                    self.measurements_stack = []
        else:
            self.measurements_stack.append(measurements)
