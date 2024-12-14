import pytest
from moto import mock_s3
import boto3

@pytest.fixture(scope="function")
def s3_mock():
    """
    Фикстура для эмуляции S3 с помощью moto.
    """
    with mock_s3():
        # Настраиваем S3
        s3 = boto3.client("s3", region_name="us-east-1")
        bucket_name = "test-bucket"
        s3.create_bucket(Bucket=bucket_name)
        yield s3
