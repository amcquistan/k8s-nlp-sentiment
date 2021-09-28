import argparse

from kafka import KafkaConsumer


def main(args):
    opts = {
      'bootstrap_servers': args.bootstrap_servers.split(',')
    }
    if args.consumer_group:
        opts.update(group_id=args.consumer_group)

    if args.from_beginning:
        opts.update(auto_offset_reset='earliest')

    consumer = KafkaConsumer(args.topic, **opts)

    for message in consumer:
        print("%s:%d:%d: key=%s value=%s" % (
              message.topic,
              message.partition,
              message.offset,
              message.key,
              message.value))



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--bootstrap-servers', required=True, help='separate with commas if multiple')
    parser.add_argument('--topic', required=True)
    parser.add_argument('--consumer-group', default='')
    parser.add_argument('--from-beginning', action='store_true', default=False)
    args = parser.parse_args()

    main(args)
