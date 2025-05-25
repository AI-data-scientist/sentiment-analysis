import tweepy
import json
import logging
import time
from kafka import KafkaProducer

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Twitter API
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAMji1wEAAAAASIDE1MRiAK4moMFZwZN9w8oHVaA%3D4PJ0ycQ8uVnJyvgz14n9Y7yY6JQ0Q847eXMTvf590cgKWGAyfE"  # Replace with your bearer token# Kafka

KAFKA_BOOTSTRAP_SERVERS = 'kafka:29092'
KAFKA_TOPIC = 'tweets'

def initialize_kafka_producer():
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        logger.info("Kafka producer ready.")
        return producer
    except Exception as e:
        logger.error(f"Failed to initialize Kafka producer: {e}")
        raise

def fetch_tweets(client, query, max_results=10):
    try:
        tweets = client.search_recent_tweets(
            query=query,
            max_results=max_results,
            tweet_fields=['created_at', 'lang']
        )
        return tweets.data if tweets.data else []
    except tweepy.TweepyException as e:
        logger.error(f"Twitter API error: {e}")
        if '429' in str(e):
            logger.warning("Rate limit hit. Sleeping 15 minutes...")
            time.sleep(15 * 60)
            return fetch_tweets(client, query, max_results)
        return []

def main():
    client = tweepy.Client(bearer_token=BEARER_TOKEN)
    producer = initialize_kafka_producer()
    query = "morocco lang:en -is:retweet"

    while True:
        tweets = fetch_tweets(client, query, max_results=10)

        if not tweets:
            logger.warning("No tweets found.")
        else:
            for tweet in tweets:
                logger.info(f"Tweet: {tweet.text}")
                message = {
                    'text': tweet.text,
                    'created_at': tweet.created_at.isoformat()  # Add the timestamp
                }
                try:
                    producer.send(KAFKA_TOPIC, message)
                    logger.info(f"Sent to Kafka: {message}")
                except Exception as e:
                    logger.error(f"Failed to send message: {e}")
                time.sleep(1)

        logger.info("Waiting 20s before next fetch")
        time.sleep(20)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info(" Producer interrupted by user.")
    except Exception as e:
        logger.error(f" Producer crashed: {e}")
    finally:
        logger.info("Shutting down producer.")
