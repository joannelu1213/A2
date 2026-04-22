import json
import boto3
import requests
from botocore.exceptions import ClientError

# S3 setup
s3 = boto3.client("s3", region_name="us-east-1")
bucket_name = "s4066477-music-images"

def upload_images():
    try:
        # Load original dataset
        with open("2026a2_songs.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        songs = data["songs"]

        # Use a set to avoid duplicate downloads
        unique_urls = set()

        for song in songs:
            unique_urls.add(song["img_url"])

        print(f"Found {len(unique_urls)} unique images.")

        # Download and upload each image
        for url in unique_urls:
            print(f"Processing: {url}")

            # Get image data
            response = requests.get(url)
            if response.status_code != 200:
                print("Failed to download image.")
                continue

            # Extract file name from URL
            file_name = url.split("/")[-1]

            # Upload to S3
            s3.put_object(
                Bucket=bucket_name,
                Key=file_name,
                Body=response.content,
                ContentType="image/jpeg"
            )

            print(f"Uploaded: {file_name}")

        print("All images uploaded successfully.")

    except FileNotFoundError:
        print("Dataset file not found.")

    except ClientError as e:
        print("AWS error:")
        print(e)

    except Exception as e:
        print("Unexpected error:")
        print(e)


if __name__ == "__main__":
    upload_images()
