import unittest
from datetime import datetime
from Core.measurementsResult import MeasurementsResult


class TestRunMeasurements(unittest.TestCase):

    def test_init(self):
        # test success call for init
        m_result = ['1', 2]
        mr = MeasurementsResult(m_result)
        self.assertIsInstance(mr.result, cls=list)
        self.assertEqual(mr.result, m_result)
        self.assertIsInstance(mr.time, cls=datetime)


if __name__ == '__main__':
    unittest.main()
