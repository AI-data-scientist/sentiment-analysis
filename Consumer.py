from pyspark.sql import SparkSession
from pyspark.ml import PipelineModel
from pyspark.sql.functions import from_json, col, udf
from pyspark.sql.types import StructType, StringType, IntegerType
import re

# Define input Kafka schema
schema = StructType().add("text", StringType())

# Load your trained pipeline model
pipeline = PipelineModel.load("logistic_regression_model.pkl")

# Create Spark session with proper MongoDB config
spark = SparkSession.builder \
    .appName("KafkaToMongoWithModel") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.3.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
    .config("spark.mongodb.write.connection.uri", "mongodb://admin:admin123@mongodb:27017") \
    .config("spark.mongodb.read.connection.uri", "mongodb://admin:admin123@mongodb:27017") \
    .config("spark.mongodb.database", "tweets_db") \
    .config("spark.mongodb.collection", "tweets") \
    .getOrCreate()

# Clean text function
def clean_text(text):
    text = re.sub(r'https?://\S+|www\.\S+|\.com\S+|youtu\.be/\S+', '', text)
    text = re.sub(r'(@|#)\w+', '', text)
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

clean_udf = udf(clean_text, StringType())

# Map numerical prediction to sentiment label
def map_sentiment(index):
    mapping = {0: "Negative", 1: "Positive", 2: "Neutral", 3: "Irrelevant"}
    return mapping.get(index, "Unknown")

map_udf = udf(map_sentiment, StringType())

# Read from Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:29092") \
    .option("subscribe", "tweets") \
    .load()

# Parse Kafka JSON message
tweets_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Apply preprocessing and prediction
tweets_cleaned = tweets_df.withColumn("cleaned_text", clean_udf(col("text")))
predicted_df = pipeline.transform(tweets_cleaned.select(col("cleaned_text").alias("Text")))

# Add sentiment label
final_df = predicted_df.withColumn("sentiment", map_udf(col("prediction"))) \
    .select(col("Text").alias("text"), "sentiment")

# Write results to MongoDB with explicit connection options
query = final_df.writeStream \
    .format("mongodb") \
    .option("checkpointLocation", "/app/checkpoint") \
    .option("spark.mongodb.connection.uri", "mongodb://admin:admin123@mongodb:27017") \
    .option("spark.mongodb.database", "tweets_db") \
    .option("spark.mongodb.collection", "tweets") \
    .outputMode("append") \
    .start()
    
query.awaitTermination()