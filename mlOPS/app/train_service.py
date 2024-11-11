# app/train_service.py
import grpc
from concurrent import futures
import joblib
import logging
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import make_classification
import train_service_pb2
import train_service_pb2_grpc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

available_models = {"decision_tree": DecisionTreeClassifier, "random_forest": RandomForestClassifier}
trained_models = {}

class TrainService(train_service_pb2_grpc.TrainServiceServicer):
    def TrainModel(self, request, context):
        model_type = request.model_type
        parameters = {k: v for k, v in request.parameters.items()}
        model_class = available_models.get(model_type)
        if not model_class:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Model type not supported")
            return train_service_pb2.TrainResponse()

        model = model_class(**parameters)
        X, y = make_classification(n_samples=100, n_features=4)
        model.fit(X, y)
        
        model_id = f"{model_type}_{len(trained_models) + 1}"
        trained_models[model_id] = model
        joblib.dump(model, f"models/{model_id}.joblib")
        logger.info(f"Model {model_id} trained and saved.")
        return train_service_pb2.TrainResponse(model_id=model_id, message="Model trained successfully.")

    def PredictModel(self, request, context):
        model_id = request.model_id
        if model_id not in trained_models:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Model not found")
            return train_service_pb2.PredictResponse()

        model = trained_models[model_id]
        prediction = model.predict([request.data])
        logger.info(f"Prediction made by model {model_id}: {prediction}")
        return train_service_pb2.PredictResponse(prediction=prediction.tolist())

    def GetAvailableModels(self, request, context):
        return train_service_pb2.ModelList(models=list(available_models.keys()))

    def DeleteModel(self, request, context):
        model_id = request.model_id
        if model_id in trained_models:
            del trained_models[model_id]
            joblib.os.remove(f"models/{model_id}.joblib")
            logger.info(f"Model {model_id} deleted.")
            return train_service_pb2.ModelResponse(message="Model deleted successfully.")
        
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details("Model not found")
        return train_service_pb2.ModelResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    train_service_pb2_grpc.add_TrainServiceServicer_to_server(TrainService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    logger.info("gRPC server started on port 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
