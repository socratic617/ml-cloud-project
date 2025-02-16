"""
    Pytest fixture to mock AWS services.
"""
import os
from typing import Generator
import boto3
from pytest import fixture

# from tests.consts import TEST_BUCKET_NAME
from moto import mock_aws
from files_api.main import S3_BUCKET_NAME as TEST_BUCKET_NAME

#Set the enviornment variables to point away from AWS
def point_away_from_aws() -> None:
    """
        Mock env variables
    """
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
    os.environ["AWS_ENDPOINT_URL"] = "http://localhost:5001"

@fixture(scope="function")
def mocked_aws() -> Generator[None,None,None]:
    """
    Set up a mocked AWS enviornment for testing and clean up after the test
    """
    with mock_aws():
        # Set the enviornment variables to point away from AWS
        point_away_from_aws()

        # Create an s3 bucket
        s3_client = boto3.client("s3")
        response = s3_client.list_buckets()
        print("BEFORE Available Buckets:", response["Buckets"])
        s3_client.create_bucket(
            Bucket=TEST_BUCKET_NAME
        )
        response = s3_client.list_buckets()
        print("AFTER Available Buckets:", response["Buckets"])
        yield

        # Delete all objects in the bucket and the bucket itself
        response =  s3_client.list_objects_v2(Bucket=TEST_BUCKET_NAME)
        for obj in response.get("Contents", []):
            s3_client.delete_object(Bucket=TEST_BUCKET_NAME, Key=obj["Key"])

        s3_client.delete_bucket(Bucket=TEST_BUCKET_NAME)

        print("Hello from cleanup")
