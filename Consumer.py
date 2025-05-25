import sys
import os
import re
import grpc
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf, pandas_udf
from pyspark.sql.types import StructType, StringType
import pandas as pd

#  Chemin vers les fichiers gRPC générés dans le dossier core de XEmotion
sys.path.append(os.path.join(os.path.dirname(__file__), "XEmotion", "core"))

import sentiment_pb2
import sentiment_pb2_grpc

#  1. Définir le schéma Kafka
schema = StructType().add("text", StringType())

#  2. Créer une session Spark
spark = SparkSession.builder \
    .appName("KafkaToMongoWithGrpcModel") \
    .config("spark.jars.packages", 
        "org.mongodb.spark:mongo-spark-connector_2.12:10.3.0,"
        "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
    .config("spark.mongodb.write.connection.uri", "mongodb://admin:admin123@mongodb:27017") \
    .config("spark.mongodb.read.connection.uri", "mongodb://admin:admin123@mongodb:27017") \
    .config("spark.mongodb.database", "tweets_db") \
    .config("spark.mongodb.collection", "tweets") \
    .getOrCreate()

#  3. Nettoyage du texte
def clean_text(text):
    text = re.sub(r'https?://\S+|www\.\S+|\.com\S+|youtu\.be/\S+', '', text)
    text = re.sub(r'(@|#)\w+', '', text)
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

clean_udf = udf(clean_text, StringType())

#  4. UDF pour appeler le service gRPC
@pandas_udf("string")
def grpc_predict_udf(cleaned_text_series):
    sentiments = []
    try:
        channel = grpc.insecure_channel("grpc-ml-model:50052")
        stub = sentiment_pb2_grpc.SentimentAnalyzerStub(channel)

        for text in cleaned_text_series:
            request = sentiment_pb2.TextRequest(text=text)
            response = stub.AnalyzeText(request)
            sentiments.append(response.sentiment)

    except Exception as e:
        print("Erreur gRPC:", str(e))
        sentiments = ["Unknown"] * len(cleaned_text_series)

    return pd.Series(sentiments) 

# 5. Lire depuis Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:29092") \
    .option("subscribe", "tweets") \
    .load()

# 6. Parser les messages JSON
tweets_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# 7. Pipeline Spark + gRPC
tweets_cleaned = tweets_df.withColumn("cleaned_text", clean_udf(col("text")))
predicted_df = tweets_cleaned.withColumn("sentiment", grpc_predict_udf(col("cleaned_text")))
final_df = predicted_df.select(col("text"), col("sentiment"))

# 8. Écrire dans MongoDB
query = final_df.writeStream \
    .format("mongodb") \
    .option("checkpointLocation", "/app/checkpoint") \
    .option("spark.mongodb.connection.uri", "mongodb://admin:admin123@mongodb:27017") \
    .option("spark.mongodb.database", "tweets_db") \
    .option("spark.mongodb.collection", "tweets") \
    .outputMode("append") \
    .start()

query.awaitTermination()