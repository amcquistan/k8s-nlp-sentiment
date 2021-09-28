import argparse
import atexit
import logging
import sys
import time

from kafka import KafkaProducer
from kafka.errors import KafkaError

stdout_handler = logging.StreamHandler(sys.stdout)
stderr_handler = logging.StreamHandler(sys.stderr)
handlers = [stdout_handler, stderr_handler]

logging.basicConfig(
    level=logging.DEBUG, 
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=handlers
)

logger = logging.getLogger(__name__)

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
            logger.info(log_msg)


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
            logger.error(log_msg, exc_info=err)


def main(args):
    producer = KafkaProducer(bootstrap_servers=args.bootstrap_servers.split(','))

    atexit.register(lambda p: p.flush(), producer)

    print("Establishing connection")
    time.sleep(5) # wait for connection to be established

    print("Enter messages")
    while True:
      msg = input("Message: ")
      bytes_data = msg.encode('utf-8')
      producer.send(args.topic, bytes_data)\
              .add_callback(SuccessCallback(msg))\
              .add_errback(ErrCallback(msg))



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--bootstrap-servers', required=True, help='separate with commas if multiple')
    parser.add_argument('--topic', required=True)
    args = parser.parse_args()

    main(args)
 