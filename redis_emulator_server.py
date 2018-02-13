#!/usr/bin/env python

"""
usage: redis_emulator_server.py [-h] [-a REDIS_HOST] [-p REDIS_PORT]

Redis Server Emulator

optional arguments:
  -h, --help            show this help message and exit
  -a REDIS_HOST, --redis_host REDIS_HOST
                        Redis host address
  -p REDIS_PORT, --redis_port REDIS_PORT
                        Redis port address

"""

import sys
import argparse
import socket

import thread

DEFAULTS = {
    'redis_host': '127.0.0.1',
    'redis_port': '10000'
}


def parse_args():
    """

    :return:
    """
    parser = argparse.ArgumentParser(description='Redis Server Emulator')
    parser.add_argument('-a', '--redis_host',
                        help='Redis host address',
                        default=DEFAULTS['redis_host'])
    parser.add_argument('-p', '--redis_port',
                        help='Redis port address',
                        default=DEFAULTS['redis_port'])

    return parser.parse_args()


class RedisEmulatorServer(socket.socket):
    """
    Simple socket server who broadcast sent messages
    """
    clients = []

    def __init__(self, host, port):
        super(RedisEmulatorServer, self).__init__()
        self.port = port
        self.host = host
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.bind((self.host, self.port))
        self.listen(15)

    def run(self):
        """
        Run server

        :return:
        """
        print >> sys.stderr, "<< Server started on {}:{} >>".format(self.host,
                                                                    self.port)
        self.register_client()

    def stop(self):
        """
        Stop server

        :return:
        """
        print >> sys.stderr, "<< Server closed >>"
        for client in self.clients:
            client.close()
        self.close()

    def register_client(self):
        """
        Adds new client

        :return:
        """
        while True:
            (clientsocket, address) = self.accept()
            print >> sys.stderr, '<< Client registered {} >>'.format(address)
            self.clients.append(clientsocket)
            thread.start_new_thread(self.receive, (clientsocket,))

    def receive(self, client):
        """
        Receives messages and broadcast them if are "messages" type

        :param client:
        :return:
        """
        while True:
            data = client.recv(4095)
            if data == '':
                break
            if self.to_broadcast(data):
                print >> sys.stderr, '\r\n<< BROADCASTING MESSAGE >>'
                print >> sys.stderr, '-' * 50
            print >> sys.stderr, data

            if self.to_broadcast(data):
                self.broadcast(data)
                self.clients.remove(client)
                client.close()
                thread.exit()

    @staticmethod
    def to_broadcast(msg):
        """

        :param msg:
        :return:
        """
        return '$7' in msg and (
            'message' in msg.lower() or 'publish' in msg.lower())

    def broadcast(self, message):
        """
        Broadcast a message to all registered clients

        :param message:
        :return:
        """
        for client in self.clients:
            client.send(message)


def main(_args, server_class):
    """

    :param server_class:
    :param _args:
    :return:
    """
    redis_host = _args['redis_host']
    redis_port = int(_args['redis_port'])

    server = server_class(redis_host, redis_port)

    try:
        server.run()
    except KeyboardInterrupt:
        server.stop()


if __name__ == "__main__":
    main(vars(parse_args()), RedisEmulatorServer)
