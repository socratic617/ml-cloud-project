"""
TODO
"""

# import os
import boto3
from files_api.s3.write_objects import upload_s3_object
from tests.consts import TEST_BUCKET_NAME
# from files_api.main import S3_BUCKET_NAME as TEST_BUCKET_NAME

def test__upload_s3_object(mocked_aws):

    # Upload a file to the bucket, with a particular content type
    object_key = "test.txt"
    file_content: bytes = b"Hello, world!"
    content_type = "application/octet-stream"

    s3_client = boto3.client("s3")


    upload_s3_object(
        bucket_name=TEST_BUCKET_NAME,
        object_key=object_key,
        file_content=file_content
    )

    # Check that the file was uploaded with the correct content type

    response = s3_client.get_object(Bucket=TEST_BUCKET_NAME, Key=object_key)
    assert response["ContentType"] == content_type
    assert response["Body"].read() == file_content
