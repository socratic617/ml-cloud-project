import os
import boto3
from pytest import fixture
from tests.consts import TEST_BUCKET_NAME
from moto import mock_aws

def point_away_from_aws(): 
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

@fixture
def mocked_aws():
    with mocked_aws():
        point_away_from_aws()

        # Create an s3 bucket
        s3_client = boto3.client("s3")
        s3_client.create_bucket(Bucket=TEST_BUCKET_NAME)

        yield

        # Delete all objects in the bucket and the bucket itself
        response =  s3_client.list_objects_v2(Bucket=TEST_BUCKET_NAME)
        for obj in response.get("Contents", []):
            s3_client.delete_object(Bucket=TEST_BUCKET_NAME, Key=obj["Key"])
        s3_client.delete_bucket(Bucket=TEST_BUCKET_NAME)

        print("Hello from cleanup")