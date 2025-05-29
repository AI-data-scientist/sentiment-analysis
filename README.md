# Real-Time Twitter Sentiment Analysis
------------------------------------

This project is a full pipeline for real-time sentiment analysis of tweets using Kafka, Apache Spark, MongoDB, a gRPC microservice for machine learning, and Django for visualization.

## Features:
- Live tweet collection via Twitter API (Tweepy)
- Kafka streaming pipeline
- Real-time processing with Apache Spark
- Sentiment classification using a gRPC microservice
- Storage of results in MongoDB
- Visualization through a Django dashboard

## Architecture:
Tweepy Producer → Kafka Topic → Spark Streaming → gRPC Sentiment Classifier → MongoDB → Django Dashboard

## Technologies Used:
- Python
- Apache Kafka
- Apache Spark
- gRPC (for ML microservice)
- MongoDB
- Django
- Docker & Docker Compose

How to Run the Project:

### 1. Clone the repository:

   git clone https://github.com/AI-data-scientist/sentiment-analysis.git
   cd sentiment-analysis

### 2. Set up configuration:

   Change the BEARER_TOKEN in producer:
   BEARER_TOKEN = your_BEARER_TOKEN


### 3. Start with Docker:

   docker-compose up --build


## Tests:

- To test the gRPC service:

   python sentiment_server.py

- To run Spark locally:

   spark-submit SparkPipeline.py

## Project Structure:

- producer.py
- consumer.py
- SparkPipeline.py
- sentiment.proto
- grpc_server/sentiment_server.py
- XEmotion/ (Django project)
- docker-compose.yml
- requirements.txt
- README.md

## Author:
@AI-data-scientist

## License:
MIT License
