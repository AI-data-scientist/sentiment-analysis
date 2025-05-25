
# Microservice Spark ML avec gRPC

Ce microservice gRPC expose un modèle Spark ML (PipelineModel) entraîné via une méthode RPC.

## Fichiers
- sentiment.proto : définition gRPC
- sentiment_server.py : serveur gRPC avec modèle Spark
- Dockerfile : pour lancer avec Spark + Python
- requirements.txt

## Port
Le service écoute sur le port 50052

## Compilation .proto
A faire si modifié :
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. sentiment.proto
