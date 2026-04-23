import boto3
from botocore.exceptions import ClientError

s3 = boto3.client("s3", region_name="us-east-1")

bucket_name = "s4066477-music-images"


def create_bucket():
    try:
        s3.create_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' created successfully.")

    except ClientError as e:
        if e.response["Error"]["Code"] == "BucketAlreadyOwnedByYou":
            print("Bucket already exists.")
        else:
            print("Error creating bucket:")
            print(e)


if __name__ == "__main__":
    create_bucket()
