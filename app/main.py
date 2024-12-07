from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
import logging
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import make_classification
import os

app = FastAPI()

# Логгер
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
