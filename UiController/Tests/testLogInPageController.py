import unittest
from UiController import logInPageController as lc


class TestHealthCheckPageController(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('setupClass')

    @classmethod
    def tearDownClass(cls):
        print('teardownClass')

    def setUp(self):
        print('setUp')
        self.lc = lc.LoginController('Alex Shahor,', '123456789')

    def tearDown(self):
        print('tearDown\n')

    def test_check_validation_name(self):
        print('test_get_health_map')
        res = self.lc.check_validation('Name', 'asd')
        self.assertEqual(res, 'Please enter a full name with space.')

        res = self.lc.check_validation('Name', 'asd ')
        self.assertEqual(res, 'Please enter a full name.')

        res = self.lc.check_validation('Name', 'asd hg6')
        self.assertEqual(res, 'Name should not contain any numbers')

        res = self.lc.check_validation('Name', 'asd hg')
        self.assertEqual(res, 'OK')

    def test_check_validation_if(self):
        print('test_get_health_map')
        res = self.lc.check_validation('Id', '123')
        self.assertEqual(res, 'ID need to be at len 9.')

        res = self.lc.check_validation('Id', '12345678y')
        self.assertEqual(res, 'ID should not contain any letters.')

        res = self.lc.check_validation('Id', '123456789')
        self.assertEqual(res, 'OK')


if __name__ == '__main__':
    unittest.main()
