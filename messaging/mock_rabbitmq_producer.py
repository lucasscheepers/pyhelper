import logging

log = logging.getLogger("messaging/mock_rabbitmq_producer.py")


class MockRabbitMqProducer:
    def produce_gitlab_data(self, body):
        """Mocks the RabbitMqProducer"""
        log.info(f"Sent the data to a Mock queue with the following variables: {body}")
