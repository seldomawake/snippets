import re
from boto3 import client


class S3Utilities:

    def __init__(self):
        pass

    # we are relying on boto3 to authenticate, etc.
    # http://boto3.readthedocs.io/en/latest/guide/configuration.html
    @staticmethod
    def list_buckets():
        connection = client('s3')
        bucket_list = connection.list_buckets()
        return [x['Name'] for x in bucket_list['Buckets']]

    @staticmethod
    def get_all_keys_in_bucket(bucket_name):
        assert isinstance(bucket_name, str)
        # get list of files in bucket
        conn = client('s3')
        paginator = conn.get_paginator('list_objects')
        operation_parameters = {'Bucket': bucket_name}
        page_iterator = paginator.paginate(**operation_parameters)
        toret = []
        for page in page_iterator:
            files_in_page = [file['Key'] for file in page["Contents"]]
            toret.extend(files_in_page)

        return toret

    @staticmethod
    def find_files_in_bucket(bucket_name, substring_to_match=''):
        # find objects matching pattern
        keys_in_bucket = S3Utilities.get_all_keys_in_bucket(bucket_name=bucket_name)
        matches = [f for f in keys_in_bucket if substring_to_match in f]
        return matches
