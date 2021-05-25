import config
from Services import healthChecksService as hcs


class HealthCheckPageController:

    def __init__(self):
        """
        init function for the status of the program and the health list.
        """
        self.ready = True
        self.health_list = health_list_tests() if config.DEBUG else hcs.run_health_checks()
        self.health_dict = {}

    def get_health_map(self):
        """
        create a health map from the health list.
        :return: self.health_dict: health map for each component what is status
        """
        for i in range(len(self.health_list)):
            val = self.health_list[i]
            try:
                key = list(val.keys())[0].split('is_')[1].replace('_', ' ').upper()
            except:
                key = list(val.keys())[0].replace('_', ' ').upper()
            val = list(val.values())[0]
            self.health_dict.update({key: val})
            print(val, key) if config.DEBUG else None
        return self.health_dict

    def is_ready(self):
        """
        check if all health components are ready to run.
        :return: self.ready: a boolean indicating if the process is ready or not
        """
        for key, val in self.health_dict.items():
            if not val:
                self.ready = False
        return self.ready


def health_list_tests():
    """
    function for tests.
    :return: a list that mimics the operation of the service get health.
    """
    return [{'is_zoom_installed': True}, {'is_manycam_installed': True},
            {'is_manycam_running': True}, {'is_alive': True}, {'camera_source': True}]


if __name__ == '__main__':
    x = HealthCheckPageController()
    x.get_health_map()
    print(x.is_ready())