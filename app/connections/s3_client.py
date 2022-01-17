import boto3
from singleton_decorator import singleton
import pickle
import os


@singleton
class S3Client:
    """S3 client for connecting with AWS S3."""
    def __init__(self):
        self.s3 = boto3.client('s3',
                               region_name='eu-west-2',
                               aws_access_key_id=os.environ['AMAZON_ACCESS_KEY_ID'],
                               aws_secret_access_key=os.environ['AMAZON_SECRET_ACCESS_KEY'])

    def read_most_recent_model(self):
        """Get the most recent version of the model from AWS S3 for exposing in API endpoint."""
        model_links = self.s3.list_objects_v2(Bucket='funda-airflow', Prefix='models')

        if len(model_links.get('Contents')) > 1:
            # Get the last modified filename
            model_links = model_links['Contents'][1:]
            last_added = [link_obj for link_obj in sorted(model_links, key=self._get_last_modified, reverse=True)][0]

            # Get last added file content as a model
            last_added_link = last_added['Key']
            model_object = self.s3.get_object(Bucket='funda-airflow', Key=last_added_link)
            model = pickle.loads(model_object['Body'].read())
            return model
        else:
            raise Exception('Exception')

    @staticmethod
    def _get_last_modified(obj):
        return int(obj['LastModified'].strftime('%s'))
