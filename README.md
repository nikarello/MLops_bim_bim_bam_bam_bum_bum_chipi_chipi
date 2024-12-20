
# Команда №22  
Михайлов Никита ┬┴┬┴┤( ͡° ͜ʖ├┬┴┬┴  
Михаил Евдокимов (×﹏×)  

Пока мы выполняли его - мы порвали обе ж. No homo, just simple (NOT) mlops.  

Этот проект представляет собой расширенное API для управления данными, обучения и использования моделей машинного обучения. Теперь добавлена интеграция с MinIO для работы с хранилищем данных и DVC для управления версиями данных. Поддерживается загрузка данных, управление версиями, обучение моделей, предсказания, удаление обученных моделей и настройка гиперпараметров.  

## Стек технологий ╰(▔∀▔)╯  
- **FastAPI** — REST API  
- **gRPC** — процедурный API  
- **DVC** — управление версиями данных  
- **MinIO** — S3-совместимое хранилище  
- **Streamlit** — интерактивный дашборд  
- **Scikit-Learn** — модели ML  
- **Joblib** — сохранение моделей  

## Установка (o･ω･o)  
1. Клонируйте репозиторий и перейдите в директорию проекта:  
    ```bash
    git clone https://github.com/yourusername/yourproject.git  
    cd yourproject  
    ```  
2. Установите зависимости:  
    ```bash
    pip install -r requirements.txt  
    ```  

## Настройка MinIO и DVC  
1. Запустите MinIO:  
    ```bash
    docker network create mlops-network  
    docker run -d --name minio --network mlops-network -p 9000:9000 -p 9001:9001         -e "MINIO_ROOT_USER=admin"         -e "MINIO_ROOT_PASSWORD=password"         quay.io/minio/minio server /data --console-address ":9001"  
    ```  

2. Создайте bucket в MinIO:  
   - Перейдите в веб-интерфейс по адресу: [http://localhost:9001](http://localhost:9001)  
   - Логин: `admin`, пароль: `password`.  
   - Создайте bucket с именем `dvc-bucket`.  

3. Настройте DVC для подключения к MinIO:  
    ```bash
    dvc remote add -d myremote s3://dvc-bucket
    dvc remote modify myremote endpointurl http://localhost:9000
    dvc remote modify myremote access_key_id admin
    dvc remote modify myremote secret_access_key password
    ```

## Запуск o(>ω<)o  

### 1. **Запуск в Docker**  
- Соберите Docker-образ:  
    ```bash
    docker build -t mlops-app .  
    ```  

- Запустите приложение:  
    ```bash
    docker run -d --name mlops-app --network mlops-network -p 8000:8000         -e AWS_ACCESS_KEY_ID=admin         -e AWS_SECRET_ACCESS_KEY=password         mlops-app  
    ```  

### 2. **Обучение модели и управление данными**  
1. Добавьте данные для обучения:  
    ```bash
    dvc add data/test_data.txt  
    git add data/test_data.txt.dvc  
    git commit -m "Add training data"  
    dvc push  
    ```  

2. Создайте и запустите процесс обучения:  
    ```bash
    dvc stage add -n train -d data/test_data.txt -d src/train.py -o models/model.pkl python src/train.py
    dvc repro  
    dvc push  
    ```  

## Использование ٩(｡•́‿•̀｡)۶  

### REST API  
- **`/upload`** (POST) — Загрузка файла в MinIO  
- **`/dvc/add`** (POST) — Добавление файла в управление DVC  
- **`/dvc/push`** (POST) — Загрузка данных в удалённое хранилище через DVC  
- **`/train`** (POST) — Обучение модели с гиперпараметрами  
- **`/predict`** (POST) — Предсказание для модели по `model_id`  
- **`/delete_model/{model_id}`** (DELETE) — Удаление модели  
- **`/models`** (GET) — Список доступных типов моделей  
- **`/status`** (GET) — Проверка статуса сервиса  

### Примеры запросов (◕‿◕)  

#### Загрузка файла  
```bash
curl -X POST "http://127.0.0.1:8000/upload" -F "file=@test_upload.txt"  
```

#### Добавление файла в DVC 
```bash
curl -X POST "http://127.0.0.1:8000/dvc/add" -H "Content-Type: application/json" -d "{"file_path": "data/test_data.txt"}"
```
#### Обучение модели
```bash
curl -X POST "http://127.0.0.1:8000/train" -H "Content-Type: application/json" -d "{"type_of_model": "decision_tree", "parameters": {"max_depth": 5}}"  
```

#### Push данных через DVC
```bash
curl -X POST "http://127.0.0.1:8000/dvc/push"   
```

Дополнительно (・∀・)
Swagger-документация доступна по адресу: http://127.0.0.1:8000/docs
gRPC-интерфейсы описаны в train_service.proto.

v1:
Что говорит японец салату из морских водорослей на Фукусиме?
Тише, чука! :)

v2:
Пациент очень волнуется перед операцией. Хирург его успокаивает:
— Я делал такую операцию уже 255 раз.
Больной облегченно испускает дух прямо на операционном столе. Пациент был восьмибитным :) :)

v3:
Если у тебя нет отца, значит у кого то их два :) :) :)


 
