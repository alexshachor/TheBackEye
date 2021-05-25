import config


class HealthCheckPageController:

    def __init__(self):
        self.ready = True
        self.health_list = health_list_tests()
        self.health_dict = {}

    def get_health_map(self):
        pass

    def is_ready(self):
        pass


def health_list_tests():
    pass


if __name__ == '__main__':
    x = HealthCheckPageController()
    x.get_health_map()
    print(x.is_ready())
