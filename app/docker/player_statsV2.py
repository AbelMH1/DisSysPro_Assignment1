import functools
import json
import os
import sys
import pika

from patterns import player_stats_dao_thread_safe_singleton

import socket

HOST = '0.0.0.0'
PORT = 64000

'''
def callback(ch, method, properties, body):
    dao = player_stats_dao_thread_safe_singleton.PlayerStatsDao.get_instance()
    ret = dao.add(json.loads(body))
    print(" [x] Received " + ret)
    properties.sendall(ret.encode())
'''


def myCallback(ch, method, properties, body, conn):
    dao = player_stats_dao_thread_safe_singleton.PlayerStatsDao.get_instance()
    ret = dao.add(json.loads(body))
    print(" [x] Received " + ret)
    conn.sendall(ret.encode())


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen()
        print("Server started, listening on " + str(PORT))
        conn, addr = sock.accept()
        with conn:
            print('Connected from: ', addr)
            while True:
                data = conn.recv(512).decode()
                if not data:
                    break
                conn.sendall('Starting to receive data...'.encode())

                connection = pika.BlockingConnection(pika.ConnectionParameters(HOST))
                channel = connection.channel()
                channel.queue_declare(queue='player-stats')
                # Now I make use of partial functions to create a callback function passing an extra parameter
                callback = functools.partial(myCallback, conn=conn)
                channel.basic_consume(queue='player-stats',
                                      auto_ack=True,
                                      on_message_callback=callback)

                print(' [*] Waiting for messages. To exit press CTRL+C')
                channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
