import os
from src.s3_utils import upload_to_s3, download_from_s3

def test_upload_and_download():
    # Путь к тестовому файлу
    test_file = "test.txt"
    bucket_name = "test-bucket"
    object_name = "uploaded_test.txt"
    downloaded_file = "downloaded_test.txt"

    # Создаем тестовый файл
    with open(test_file, "w") as f:
        f.write("This is a test file for S3 operations.")

    try:
        # Загружаем файл в MinIO
        upload_to_s3(bucket_name, test_file, object_name)

        # Загружаем файл обратно
        download_from_s3(bucket_name, object_name, downloaded_file)

        # Проверяем, что содержимое загруженного файла совпадает с оригиналом
        with open(downloaded_file, "r") as f:
            content = f.read()

        assert content == "This is a test file for S3 operations.", "Downloaded file content mismatch."

    finally:
        # Удаляем тестовые файлы
        if os.path.exists(test_file):
            os.remove(test_file)
        if os.path.exists(downloaded_file):
            os.remove(downloaded_file)

    print("Test passed: upload and download operations successful!")
