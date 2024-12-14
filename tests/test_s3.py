import tempfile


def test_upload_to_s3(s3_mock):
    """
    Тест для загрузки файла в эмуляцию S3.
    """
    # Создаем временный файл
    with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".txt") as temp_file:
        temp_file.write("This is a test file for S3 upload.")
        temp_file_name = temp_file.name

    # Загружаем временный файл в S3
    with open(temp_file_name, "rb") as f:
        s3_mock.upload_fileobj(
            Fileobj=f,
            Bucket="test-bucket",
            Key="test_file.txt",
        )

    # Проверяем, что файл успешно загружен
    response = s3_mock.list_objects(Bucket="test-bucket")
    assert "Contents" in response
    assert response["Contents"][0]["Key"] == "test_file.txt"


def test_download_from_s3(s3_mock):
    """
    Тест для загрузки объекта из S3.
    """
    # Создаем объект в S3
    s3_mock.put_object(
        Bucket="test-bucket",
        Key="test_file.txt",
        Body="This is a test file",
    )

    # Загружаем объект обратно
    obj = s3_mock.get_object(Bucket="test-bucket", Key="test_file.txt")
    content = obj["Body"].read().decode("utf-8")
    assert content == "This is a test file"
