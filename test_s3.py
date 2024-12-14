def test_upload_to_s3(s3_mock):
    # Загрузка тестового файла в S3
    s3_mock.upload_fileobj(
        Fileobj=open("tests/test_file.txt", "rb"),
        Bucket="test-bucket",
        Key="test_file.txt",
    )

    # Проверяем, что файл успешно загружен
    response = s3_mock.list_objects(Bucket="test-bucket")
    assert "Contents" in response
    assert response["Contents"][0]["Key"] == "test_file.txt"

def test_download_from_s3(s3_mock):
    # Создаем объект в S3
    s3_mock.put_object(
        Bucket="test-bucket",
        Key="test_file.txt",
        Body="This is a test file",
    )

    # Загружаем его обратно
    obj = s3_mock.get_object(Bucket="test-bucket", Key="test_file.txt")
    content = obj["Body"].read().decode("utf-8")
    assert content == "This is a test file"
