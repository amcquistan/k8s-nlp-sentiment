import atexit
import json
import logging
import os
import sys

import redis

from flask import Flask, render_template, request, jsonify

from kafka import KafkaProducer


stdout_handler = logging.StreamHandler(sys.stdout)
stderr_handler = logging.StreamHandler(sys.stderr)
handlers = [stdout_handler, stderr_handler]

logging.basicConfig(
    level=logging.INFO, 
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=handlers
)

app = Flask(__name__)


def make_kafka_producer():
    import time
    time.sleep(10) # make sure kafka is up
    producer = KafkaProducer(bootstrap_servers=[os.environ['BOOTSTRAP_SERVER']])
    atexit.register(lambda p: p.flush(), producer)
    return producer

producer = make_kafka_producer()


redis_client = redis.Redis(host=os.environ['REDIS_HOST'], port=6379)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/analyze-text', methods=('POST',))
def analyze_text():
    request_data = request.get_json()
    url = request_data['url']

    try:
        producer.send(os.environ['KAFKA_TOPIC'], url.encode('utf-8'))\
            .add_callback(SuccessCallback(url))\
            .add_errback(ErrCallback(url))
        redis_client.delete(url)

        return jsonify({'status': 'submitted', 'message': 'submitted for analysis {url}'.format(url=url)})
    except Exception as e:
        app.logger.error("Error submitting url", exc_info=e)

    return jsonify({'status': 'failed'})


@app.route("/analysis-results")
def analysis_results():
    url = request.args.get('url')
    results = {}
    try:
        results = json.loads(redis_client.get(url).decode('utf-8'))
    except Exception as e:
        app.logger.error("Error fetching results", exc_info=e)

    return jsonify(results)


class SuccessCallback:
    def __init__(self, message, key=None, log=False):
        self.message = message
        self.key = key
        self.log = log

    def __call__(self, record_metadata):
        if self.log:
            log_msg = "\n".join([
              'Published Message:',
              '  Topic: {}'.format(record_metadata.topic),
              '  Partition: {}'.format(record_metadata.partition),
              '  Content: {}'.format(self.message),
              ''
            ])
            app.logger.info(log_msg)


class ErrCallback:
    def __init__(self, message, key=None, log=True):
        self.message = message
        self.key = key
        self.log = log

    def __call__(self, err):
        if self.log:
            log_msg = "\n".join([
              'Failed Message:',
              '  Content: {}'.format(self.message),
              ''
            ])
            app.logger.error(log_msg, exc_info=err)

