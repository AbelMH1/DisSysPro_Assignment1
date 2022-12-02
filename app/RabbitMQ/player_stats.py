import json
import os
import sys

import pika

from app.RabbitMQ import player_stats_dao_thread_safe_singleton


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
