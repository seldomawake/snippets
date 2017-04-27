import sys
import unittest
import os.path

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from JsonToCsvUngrouper import JsonToCsvUngrouper


class TestJsonToCsvUngrouper(unittest.TestCase):
    def test_csv_read(self):
        # print('current path' + os.path.dirname(__file__))
        j = JsonToCsvUngrouper('./test.csv', 'col_2')
        self.assertIsNotNone(j)
        try:
            j.read_csv()
            self.assertTrue(3 in j.col_nums_to_explode)
        except Exception as e:
            print e
            self.fail()


if __name__ == '__main__':
    unittest.main()
