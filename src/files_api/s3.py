import boto3

BUCKET_NAME = "ml-cloud-bucket-erik"

s3_client = boto3.client("s3")

#write a file to the s3 Bucket with the content "Hello, World!"
s3_client.put_object(
    Bucket=BUCKET_NAME,
    Key="folder/hello.txt",
    Body="Hello, World!",
    ContentType="text/plain",
)
