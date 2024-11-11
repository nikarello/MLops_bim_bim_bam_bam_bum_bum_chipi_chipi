Этот проект представляет собой API для обучения и использования моделей машинного обучения с помощью REST, gRPC и дашборда на Streamlit. Поддерживаются обучение моделей, предсказания, удаление обученных моделей, а также настройка гиперпараметров.

## Стек технологий ╰(▔∀▔)╯
- **FastAPI** — REST API
- **gRPC** — процедурный API
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

## Запуск o(>ω<)o
1. Запустите REST API:
    ```bash
    uvicorn app.main:app --reload
    ```
2. Запустите gRPC-сервер:
    ```bash
    python app/train_service.py
    ```
3. Запустите дашборд Streamlit:
    ```bash
    streamlit run app/dashboard.py
    ```

## Использование ٩(｡•́‿•̀｡)۶
### REST API
- **`/train`** (POST) — Обучение модели с гиперпараметрами
- **`/predict`** (POST) — Предсказание для модели по `model_id`
- **`/delete_model/{model_id}`** (DELETE) — Удаление модели
- **`/models`** (GET) — Список доступных типов моделей
- **`/status`** (GET) — Проверка статуса сервиса

### Примеры запросов (◕‿◕)
#### Обучение модели
```bash
curl -X POST "http://127.0.0.1:8000/train" -H "Content-Type: application/json" -d "{\"type_of_model\": \"decision_tree\", \"parameters\": {\"max_depth\": 5}}"
```

#### Предсказание
```bash
curl -X POST "http://127.0.0.1:8000/predict" -H "Content-Type: application/json" -d "{\"id_of_model\": \"decision_tree_1\", \"data\": [0.5, -1.2, 3.3, 0.1]}"
```
#### Спасибо (ｏ・_・)ノ”(ノ_<、) 

Swagger доступен по адресу http://127.0.0.1:8000/docs.
gRPC интерфейсы описаны в train_service.proto.

```
Что говорит японец салату из морских водорослей на Фукусиме?
-Тише, чука
```
