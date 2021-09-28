import json
import logging
import os
import sys

import redis
import requests

from bs4 import BeautifulSoup
from kafka import KafkaConsumer
from textblob import TextBlob


stdout_handler = logging.StreamHandler(sys.stdout)
stderr_handler = logging.StreamHandler(sys.stderr)
handlers = [stdout_handler, stderr_handler]
logging.basicConfig(
    level=logging.INFO, 
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=handlers
)

logger = logging.getLogger(__name__)


def main(args):
    logger.info("Started nlpconsumer")
    redis_client = redis.Redis(host=args['redis_host'], port=6379)
    consumer = KafkaConsumer(args['topic'],
                            bootstrap_servers=args['bootstrap_servers'],
                            group_id=args['consumer_group'])

    for message in consumer:
        url = message.value.decode('utf-8')
        logger.info("processing " + url)
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content)
            text = soup.get_text()
            blob = TextBlob(text)
            text_analysis = TextAnalysis(url, blob)
            redis_client.set(url, json.dumps(text_analysis.to_dict()))
        except Exception as e:
            logger.error(f"Failed analyzing {url}", exc_info=e)


class TextAnalysis:
    def __init__(self, url : str, blob : TextBlob):
        self.url = url
        self.polarity = blob.sentiment.polarity
        self.subjectivity = blob.sentiment.subjectivity
        self.nouns = [str(w) for w in blob.noun_phrases]

    def to_dict(self):
        return {
          'url': self.url,
          'polarity': self.polarity,
          'subjectivity': self.subjectivity,
          'nouns': self.nouns
        }


if __name__ == '__main__':
    import time
    time.sleep(10) # make sure other services are up
    args = {
        'bootstrap_servers': os.environ['BOOTSTRAP_SERVER'],
        'topic': os.environ['KAFKA_TOPIC'],
        'consumer_group': os.environ['CONSUMER_GROUP'],
        'redis_host': os.environ['REDIS_HOST']
    }

    main(args)


