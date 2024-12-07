from minio_client import MinioClient
from config import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_BUCKET

# Инициализация Minio-клиента
client = MinioClient(
    endpoint_url=MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    bucket_name=MINIO_BUCKET,
)

# Тест: Загрузка файла
client.upload_file("test_upload.txt", "uploaded_test_file.txt")

# Тест: Скачивание файла
client.download_file("uploaded_test_file.txt", "downloaded_test_file.txt")

# Тест: Список файлов
files = client.list_files()
print("Files in bucket:", files)
