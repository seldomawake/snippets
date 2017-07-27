import sys
import unittest
import os.path

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from S3Utilities import S3Utilities


class TestS3Utilities(unittest.TestCase):
    def test_list_buckets(self):
        buckets = S3Utilities.list_buckets()
        self.assertGreater(len(buckets), 0)

    def test_list_buckets_with_name(self):
        to_find = '*2017-02*'
        files_found = S3Utilities.find_files_in_bucket(to_match=to_find)
        self.assertGreater(len(files_found), 0)

