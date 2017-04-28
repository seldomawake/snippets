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
            j.reset_col_headers()
            self.assertTrue(3 in j.col_nums_to_explode)
        except Exception as e:
            print e
            self.fail()

    def test_file_explode(self):
        j = JsonToCsvUngrouper('./test.csv', 'col_2')
        self.assertIsNotNone(j)
        exploded_rows = []
        try:
            for r in j.get_exploded_rows():
                exploded_rows.append(r)

            self.assertEqual(7, len(exploded_rows))
            self.assertEquals(["1,000", "email@address.com", '4', 2], exploded_rows[0])
            self.assertEquals(["1,000", "email@address.com", '4', 3], exploded_rows[1])
            self.assertEquals(["1,000", "email@address.com", '4', 4], exploded_rows[2])
            self.assertEquals(["1,000", "email@address.com", '4', 5], exploded_rows[3])
            self.assertEquals(["1,001", "email@address.com", '5', 6], exploded_rows[4])
            self.assertEquals(["1,001", "email@address.com", '5', 7], exploded_rows[5])
            self.assertEquals(["1,002", "email@address.com", '1', 40], exploded_rows[6])

        except Exception as e:
            print e
            self.fail()

    def test_explode_row(self):
        j = JsonToCsvUngrouper('./test.csv', 'col_2')

        rows = [["1,000", "email@address.com", 4, "[2,3,4,5]"],
                ["1,000", "email@address.com", 4, "[6,7,8]"]]
        cols_to_explode = [3]

        splody = j.explode_rows(rows=rows, col_nums_to_explode_by=cols_to_explode)

        self.assertEquals(7, len(splody))
        self.assertEquals(["1,000", "email@address.com", 4, 2], splody[0])
        self.assertEquals(["1,000", "email@address.com", 4, 3], splody[1])
        self.assertEquals(["1,000", "email@address.com", 4, 4], splody[2])
        self.assertEquals(["1,000", "email@address.com", 4, 5], splody[3])
        self.assertEquals(["1,000", "email@address.com", 4, 6], splody[4])
        self.assertEquals(["1,000", "email@address.com", 4, 7], splody[5])
        self.assertEquals(["1,000", "email@address.com", 4, 8], splody[6])

    def test_explode_row_multiple_cols(self):
        j = JsonToCsvUngrouper('./test.csv', 'col_2')

        rows = [['["lorem", "ipsum"]', "email@address.com", 4, "[2,3,4,5]"],
                ['["1,000"]', "email@address.com", 4, "[6,7,8]"]]
        cols_to_explode = [0, 3]

        splody = j.explode_rows(rows=rows, col_nums_to_explode_by=cols_to_explode)

        self.assertEquals(11, len(splody))
        self.assertEquals(["lorem", "email@address.com", 4, 2], splody[0])
        self.assertEquals(["ipsum", "email@address.com", 4, 2], splody[1])
        self.assertEquals(["lorem", "email@address.com", 4, 3], splody[2])
        self.assertEquals(["ipsum", "email@address.com", 4, 3], splody[3])
        self.assertEquals(["lorem", "email@address.com", 4, 4], splody[4])
        self.assertEquals(["ipsum", "email@address.com", 4, 4], splody[5])
        self.assertEquals(["lorem", "email@address.com", 4, 5], splody[6])
        self.assertEquals(["ipsum", "email@address.com", 4, 5], splody[7])
        self.assertEquals(["1,000", "email@address.com", 4, 6], splody[8])
        self.assertEquals(["1,000", "email@address.com", 4, 7], splody[9])
        self.assertEquals(["1,000", "email@address.com", 4, 8], splody[10])

if __name__ == '__main__':
    unittest.main()
