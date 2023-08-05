import boto3
from botocore.exceptions import ClientError

def run():
    try:
        aws_resource=boto3.resource('s3')
        name_of_bucket=input("Please enter name of your bucket: ")
        bucket = aws_resource.Bucket(name_of_bucket)
        response = bucket.delete()
        print(response)
    except ClientError as e:
        print(e)
