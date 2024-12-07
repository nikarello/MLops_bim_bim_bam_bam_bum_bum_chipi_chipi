from fastapi import FastAPI, HTTPException, UploadFile
from pydantic import BaseModel
from enum import Enum
import logging
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import make_classification

from pydantic import BaseModel


from minio import Minio
from minio.error import S3Error
import os
import subprocess
import time

app = FastAPI()

# Логгер
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Настройки MinIO
MINIO_URL = "http://minio:9000"
MINIO_ACCESS_KEY = "admin"
MINIO_SECRET_KEY = "password"
MINIO_BUCKET = "mlops-data"

# Подключение к MinIO
minio_client = Minio(
    "minio:9000",
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

# Убедитесь, что ведро существует
while True:
    try:
        if not minio_client.bucket_exists(MINIO_BUCKET):
            minio_client.make_bucket(MINIO_BUCKET)
        break
    except S3Error as e:
        logger.warning(f"Waiting for MinIO... {e}")
        time.sleep(5)

# Список доступных моделей
available_models = {"decision_tree": DecisionTreeClassifier, "random_forest": RandomForestClassifier}
trained_models = {}

# Классы моделей
class ModelType(str, Enum):
    decision_tree = "decision_tree"
    random_forest = "random_forest"

# Запросы
class TrainRequest(BaseModel):
    type_of_model: str
    parameters: dict = {}

class PredictRequest(BaseModel):
    id_of_model: str
    data: list


class DVCAddRequest(BaseModel):
    file_path: str


@app.get("/models")
def get_available_models():
    return {"available_models": list(available_models.keys())}

@app.post("/train")
def train_model(request: TrainRequest):
    if request.type_of_model not in available_models:
        raise HTTPException(status_code=400, detail="Model type not supported")

    model_class = available_models[request.type_of_model]
    model = model_class(**request.parameters)

    # Генерация данных для обучения и обучения модели
    X, y = make_classification(n_samples=100, n_features=4)
    model.fit(X, y)

    id_of_model = f"{request.type_of_model}_{len(trained_models)+1}"
    trained_models[id_of_model] = model
    joblib.dump(model, f"{id_of_model}.joblib")

    logger.info(f"Model {id_of_model} trained and saved.")
    return {"id_of_model": id_of_model, "message": f"Model {id_of_model} trained successfully."}

@app.post("/predict")
def predict_model(request: PredictRequest):
    if request.id_of_model not in trained_models:
        raise HTTPException(status_code=404, detail="Model not found")

    model = trained_models[request.id_of_model]
    prediction = model.predict([request.data])
    
    logger.info(f"Prediction made by model {request.id_of_model}: {prediction}")
    return {"prediction": prediction.tolist()}

@app.delete("/delete_model/{id_of_model}")
def delete_model(id_of_model: str):
    if id_of_model in trained_models:
        del trained_models[id_of_model]
        os.remove(f"{id_of_model}.joblib")
        logger.info(f"Model {id_of_model} deleted.")
        return {"message": f"Model {id_of_model} deleted successfully."}
    raise HTTPException(status_code=404, detail="Model not found")

@app.get("/status")
def service_status():
    return {"status": "Service is running"}

@app.post("/upload")
async def upload_file(file: UploadFile):
    try:
        file_location = f"/tmp/{file.filename}"
        with open(file_location, "wb") as f:
            f.write(await file.read())
        minio_client.fput_object(MINIO_BUCKET, file.filename, file_location)
        os.remove(file_location)
        return {"message": f"File {file.filename} uploaded successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/dvc/add")
def add_to_dvc(request: DVCAddRequest):
    try:
        result = subprocess.run(["dvc", "add", request.file_path], check=True, capture_output=True)
        logger.info(f"File {request.file_path} added to DVC.")
        return {"message": f"File {request.file_path} added to DVC successfully.", "output": result.stdout.decode()}
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to add file to DVC: {e}")
        raise HTTPException(status_code=500, detail="Failed to add file to DVC.")

@app.post("/dvc/push")
def push_to_dvc():
    try:
        logger.info("Starting DVC push...")
        result = subprocess.run(
            ["dvc", "push"],
            check=True,
            capture_output=True,
            text=True
        )
        logger.info(f"DVC push output: {result.stdout}")
        return {"message": "Data pushed to remote storage successfully.", "output": result.stdout}
    except subprocess.CalledProcessError as e:
        logger.error(f"DVC push error: {e.stderr}")
        logger.error(f"Return code: {e.returncode}")
        logger.error(f"Command: {e.cmd}")
        raise HTTPException(status_code=500, detail=f"DVC push failed: {e.stderr}")
    except Exception as e:
        logger.error(f"Unexpected error during DVC push: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
