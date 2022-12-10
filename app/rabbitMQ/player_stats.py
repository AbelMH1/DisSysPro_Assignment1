import json
import os
import sys

import pika

from patterns import player_stats_dao_thread_safe_singleton

''' THIS CLASS IS DEPRECATED
It was used for consuming the messages from the queue generated on the wordGame_server
and saving them into a TinyDB called "player_stats.json" but know i consume the messages
using sockets when a client ask to consume them'''


def callback(ch, method, properties, body):
    dao = player_stats_dao_thread_safe_singleton.PlayerStatsDao.get_instance()
    print(" [x] Received ", end="")
    dao.add(json.loads(body))


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='player-stats')

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
