#producer.py
import tweepy
import json
import logging
import time
from kafka import KafkaProducer
from textblob import TextBlob

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Twitter API credentials
BEARER_TOKEN = ""  # Replace with your bearer token

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = 'kafka:29092'
KAFKA_TOPIC = 'tweets'

def initialize_kafka_producer():
    """Initialize and return a Kafka producer."""
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        logger.info("Kafka producer initialized successfully")
        return producer
    except Exception as e:
        logger.error(f"Failed to initialize Kafka producer: {e}")
        raise

def fetch_tweets(client, query, max_results=10):
    """Fetch tweets using Twitter API v2."""
    try:
        tweets = client.search_recent_tweets(
            query=query,
            max_results=max_results,
            tweet_fields=['created_at', 'lang']
        )
        return tweets.data if tweets.data else []
    except tweepy.TweepyException as e:
        logger.error(f"Failed to fetch tweets: {e}")
        if '429' in str(e):
            logger.info("Rate limit hit. Waiting 15 minutes...")
            time.sleep(15 * 60)  # Wait 15 minutes
            return fetch_tweets(client, query, max_results)  # Retry
        return []

def analyze_sentiment(text):
    """Analyze sentiment of the tweet text."""
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

def main():
    # Initialize Twitter API client
    client = tweepy.Client(bearer_token=BEARER_TOKEN)
    
    # Initialize Kafka producer
    producer = initialize_kafka_producer()
    
    # Twitter search query
    query = 'Maroc:retweet lang:en'
    
    # Fetch tweets
    tweets = fetch_tweets(client, query, max_results=10)
    
    if not tweets:
        logger.warning("No tweets found for the query")
        return
    
    # Process and send tweets to Kafka
    for tweet in tweets:
        logger.info(f"Tweet: {tweet.text}")
        sentiment = analyze_sentiment(tweet.text)
        message = {
            'text': tweet.text,
            'sentiment': sentiment
        }
        try:
            producer.send(KAFKA_TOPIC, message)
            logger.info(f"Sent message to Kafka: {message}")
            time.sleep(1)  # Small delay to avoid overwhelming Kafka
        except Exception as e:
            logger.error(f"Failed to send message to Kafka: {e}")
    
    # Flush producer
    producer.flush()
    logger.info("Producer flushed")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Producer stopped by user")
    except Exception as e:
        logger.error(f"Producer failed: {e}")
    finally:
        logger.info("Closing producer")
        # Producer is automatically closed by context