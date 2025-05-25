import grpc

import sys
import os
sys.path.append(os.path.dirname(__file__))  

import sentiment_pb2
import sentiment_pb2_grpc

def get_ml_sentiment(text):
    try:
        # Connexion au microservice gRPC via Docker
        channel = grpc.insecure_channel("localhost:50052")
        stub = sentiment_pb2_grpc.SentimentAnalyzerStub(channel)
        request = sentiment_pb2.TextRequest(text=text)
        response = stub.AnalyzeText(request)
        return response.sentiment, response.score
    except Exception as e:
        print("Erreur gRPC:", e)
        return "Unknown", 0.0
