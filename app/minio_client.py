import boto3
from botocore.exceptions import NoCredentialsError

class MinioClient:
    def __init__(self, endpoint_url, access_key, secret_key, bucket_name):
        self.s3 = boto3.client(
            "s3",
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )
        self.bucket_name = bucket_name

    def upload_file(self, file_path, object_name):
        """Upload a file to the S3 bucket."""
        try:
            self.s3.upload_file(file_path, self.bucket_name, object_name)
            print(f"File '{file_path}' uploaded as '{object_name}'.")
        except NoCredentialsError:
            print("Error: No credentials provided.")
        except Exception as e:
            print(f"Error uploading file: {e}")

    def download_file(self, object_name, file_path):
        """Download a file from the S3 bucket."""
        try:
            self.s3.download_file(self.bucket_name, object_name, file_path)
            print(f"File '{object_name}' downloaded to '{file_path}'.")
        except Exception as e:
            print(f"Error downloading file: {e}")

    def list_files(self):
        """List all files in the S3 bucket."""
        try:
            objects = self.s3.list_objects_v2(Bucket=self.bucket_name).get("Contents", [])
            return [obj["Key"] for obj in objects]
        except Exception as e:
            print(f"Error listing files: {e}")
            return []
