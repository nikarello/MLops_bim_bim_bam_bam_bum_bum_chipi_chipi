import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import os
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

def get_s3_client():
    """
    Создает клиент S3/MinIO с использованием переменных окружения.
    """
    try:
        return boto3.client(
            's3',
            endpoint_url=os.getenv('S3_ENDPOINT_URL'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
    except PartialCredentialsError:
        print("Error: Incomplete S3 credentials provided.")
        raise
    except NoCredentialsError:
        print("Error: S3 credentials not available.")
        raise

def upload_to_s3(bucket_name, file_path, object_name=None):
    """
    Загрузка файла в S3/MinIO.
    :param bucket_name: Название бакета.
    :param file_path: Локальный путь к файлу.
    :param object_name: Имя объекта в бакете (по умолчанию - имя файла).
    """
    s3 = get_s3_client()
    try:
        object_name = object_name or os.path.basename(file_path)
        s3.upload_file(file_path, bucket_name, object_name)
        print(f"Uploaded {file_path} to bucket {bucket_name} as {object_name}.")
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        raise
    except NoCredentialsError:
        print("Error: Credentials not available.")
        raise
    except Exception as e:
        print(f"An unexpected error occurred during upload: {e}")
        raise

def download_from_s3(bucket_name, object_name, file_path):
    """
    Загрузка файла из S3/MinIO.
    :param bucket_name: Название бакета.
    :param object_name: Имя объекта в бакете.
    :param file_path: Локальный путь для сохранения файла.
    """
    s3 = get_s3_client()
    try:
        s3.download_file(bucket_name, object_name, file_path)
        print(f"Downloaded {object_name} from bucket {bucket_name} to {file_path}.")
    except FileNotFoundError:
        print(f"Error: Local path {file_path} not found.")
        raise
    except NoCredentialsError:
        print("Error: Credentials not available.")
        raise
    except Exception as e:
        print(f"An unexpected error occurred during download: {e}")
        raise
