from unittest import mock, TestCase

from ypd import add

class TestSum(TestCase):
    def test_sum_func(self):
        a = 5.3
        b = 4

        self.assertEqual(add.sum(a, b), 9.3)