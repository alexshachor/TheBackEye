import unittest
from unittest.mock import patch
from Services import healthChecksService

class TestHealthChecksService(unittest.TestCase):

    def test_check_is_alive(self):
        with patch('requests.head') as mocled_head:
            # test success call
            mocled_head.return_value.ok = True
            result = healthChecksService.check_is_alive()
            self.assertEqual(result,{'is_server_alive': True})

            # test failure call
            mocled_head.return_value.ok = False
            result = healthChecksService.check_is_alive()
            self.assertEqual(result, {'is_server_alive': False})


    def test_check_if_program_installed(self):
        real_program = 'manycam'
        fake_program = 'blabla'

        # test success call
        result = healthChecksService.check_if_program_installed(real_program)
        self.assertEqual(result,{f'is_{real_program}_installed': True})

        # test failure call
        result = healthChecksService.check_if_program_installed(fake_program)
        self.assertEqual(result, {f'is_{fake_program}_installed': False})


    def test_check_if_process_is_running(self):
        real_process = 'manycam'
        fake_process = 'blabla'

        # test success call
        result = healthChecksService.check_if_process_is_running(real_process)
        self.assertEqual(result, {f'is_{real_process}_running': True})

        # test failure call
        result = healthChecksService.check_if_process_is_running(fake_process)
        self.assertEqual(result, {f'is_{fake_process}_running': False})

if __name__ == '__main__':
    unittest.main()