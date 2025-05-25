import sys
import os
from concurrent import futures
import grpc
from pyspark.sql import SparkSession, Row
from pyspark.ml import PipelineModel

#  1. Ajouter le chemin vers les fichiers gRPC générés
sys.path.append(os.path.join(os.path.dirname(__file__), "XEmotion", "core"))
#  2. Importer les modules gRPC
import sentiment_pb2
import sentiment_pb2_grpc

#  3. Initialiser Spark (attention à .master dans Docker)
spark = SparkSession.builder \
    .appName("MLModelService") \
    .master("local[*]") \
    .getOrCreate()

#  4. Charger le modèle ML Spark

model = PipelineModel.load("logistic_regression_model.pkl")

#  5. Implémenter le service gRPC
class SentimentService(sentiment_pb2_grpc.SentimentAnalyzerServicer):
    def AnalyzeText(self, request, context):
        text = request.text
        df = spark.createDataFrame([Row(Text=text)])
        result = model.transform(df).collect()[0]

        prediction = int(result.prediction)
        score = float(result.probability[prediction])
        sentiment = {
            0: "Negative",
            1: "Positive",
            2: "Neutral",
            3: "Irrelevant"
        }.get(prediction, "Unknown")

        return sentiment_pb2.SentimentResponse(sentiment=sentiment, score=score)

#  6. Lancer le serveur gRPC
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    sentiment_pb2_grpc.add_SentimentAnalyzerServicer_to_server(SentimentService(), server)
    server.add_insecure_port('[::]:50052')
    print("gRPC server is running on port 50052...")
    server.start()
    server.wait_for_termination()

# 7. Main
if __name__ == "__main__":
    serve()
