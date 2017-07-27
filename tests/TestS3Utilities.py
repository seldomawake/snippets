import sys
import unittest
import os.path

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from S3Utilities import S3Utilities


class TestListBuckets(unittest.TestCase):
    def test_csv_read(self):
        buckets = S3Utilities.list_buckets()
        self.assertGreater(len(buckets), 0)
