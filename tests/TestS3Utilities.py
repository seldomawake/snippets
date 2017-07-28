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
        to_find = '07_2017'
        bucket_to_test = '' # todo: use environment variable here
        files_found = S3Utilities.find_files_in_bucket(bucket_name=bucket_to_test, substring_to_match=to_find)
        # print(files_found)
        self.assertGreater(len(files_found), 0)

