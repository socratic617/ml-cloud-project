"""
    TODO
"""
import boto3

try:
    from mypy_boto3_s3 import S3Client
    from mypy_boto3_s3.type_defs import(
        PutObjectOutputTypeDef,
        # ResponseMetadataTypeDef,
    )
except ImportError:
    print("boto3-stubs[s3] is not installed")

BUCKET_NAME = "ml-cloud-bucket-erik"

session = boto3.Session()
s3_client: "S3Client" = session.client("s3")

#write a file to the s3 Bucket with the content "Hello, World!"
response: "PutObjectOutputTypeDef" = s3_client.put_object(
    Bucket=BUCKET_NAME,
    Key="folder/hello.txt",
    Body="Hello, World!",
    ContentType="text/plain",
)

# metadata : "ResponseMetadataTypeDef" = response["ResponseMetadata"]
