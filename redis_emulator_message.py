#!/usr/bin/env python

"""
usage: redis_emulator_message.py [-h] [-a REDIS_HOST] [-p REDIS_PORT]
                                 [-c REDIS_CHANNEL]

Redis Message Emulator client

optional arguments:
  -h, --help            show this help message and exit
  -a REDIS_HOST, --redis_host REDIS_HOST
                        Redis host address
  -p REDIS_PORT, --redis_port REDIS_PORT
                        Redis port address
  -c REDIS_CHANNEL, --redis_channel REDIS_CHANNEL
                        Redis pubsub channel

"""

import sys
import argparse
import redis

DEFAULTS = {
    'redis_channel': 'some_channel',
    'redis_host': '127.0.0.1',
    'redis_port': '10000'
}


def parse_args():
    parser = argparse.ArgumentParser(
        description='Redis Message Emulator client')
    parser.add_argument('-a', '--redis_host',
                        help='Redis host address',
                        default=DEFAULTS['redis_host'])
    parser.add_argument('-p', '--redis_port',
                        help='Redis port address',
                        default=DEFAULTS['redis_port'])
    parser.add_argument('-c', '--redis_channel',
                        default=DEFAULTS['redis_channel'],
                        help='Redis pubsub channel')

    return parser.parse_args()


class RedisMessageEmulator(object):
    """
    Emulates message emitted by redis pubsub
    """

    def __init__(self, host, port, channel):
        self.counter = 0
        self.channel = channel
        self.redis = redis.Redis(host=host, port=port)
        self.pubsub = self.redis.pubsub()

    def publish(self, message):
        self.redis.execute_command('message', self.channel, message)


def main(_args, pubsub_class):
    redis_host = _args['redis_host']
    redis_port = int(_args['redis_port'])
    redis_channel = _args['redis_channel']

    pubsub = pubsub_class(redis_host, redis_port, redis_channel)

    try:
        print >> sys.stderr, '<< Send to {}:{}:{}. Type \"exit\" to ' \
                             'exit>>'.format(redis_channel, redis_host,
                                             redis_port)
        _input = None
        while _input != 'exit':
            if _input is not None:
                pubsub.publish(_input)
            _input = raw_input()
            if len(_input) >= 4095:
                raise IOError('String too long!!!')
    except KeyboardInterrupt:
        print >> sys.stderr, '<<< exit >>>'
    except Exception as ex:
        print >> sys.stderr, '{}'.format(ex)


if __name__ == '__main__':
    args = parse_args()
    main(vars(args), RedisMessageEmulator)
