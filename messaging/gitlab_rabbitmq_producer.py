import pika
import json
import os
import logging

log = logging.getLogger("messaging/gitlab_rabbitmq_producer.py")


class GitLabRabbitMqProducer:
    def __init__(self):
        self.credentials = pika.PlainCredentials(os.getenv('RABBIT_USR'), os.getenv('RABBIT_PWD'))
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=os.getenv('RABBIT_HOST'), port=os.getenv('RABBIT_PORT'),
                                      credentials=self.credentials))

        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange="plugins", exchange_type="direct")
        self.channel.queue_declare(queue="gitlab")
        self.channel.queue_bind(exchange="plugins", queue="gitlab", routing_key="gitlab")

    def produce_gitlab_data(self, body):
        """Produces all the data of all the GitLab commands"""
        self.channel.basic_publish(exchange="plugins", routing_key="gitlab", body=json.dumps(body))
        log.info(f"Sent the data to the GitLab queue with the following variables: {body}")
