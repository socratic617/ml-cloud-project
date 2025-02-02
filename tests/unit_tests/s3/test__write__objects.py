
import boto3
from files_api.s3.write_objects import upload_s3_object

TEST_BUCKET_NAME = "test-bucket-mlops-club-es"
def test__upload_s3_object():
    # Create an s3 bucket 
    #upload a file to the bucket, with a particular content type
    #check that the file was uploaded witht the correct content type 
    #clean up by deleting the bucket