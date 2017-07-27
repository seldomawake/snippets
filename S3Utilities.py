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
