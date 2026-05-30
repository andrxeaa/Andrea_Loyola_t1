import pika
import os
import json
import logging
from src.core.entities import Transaction
from src.core.use_cases import MessagePublisher

logger = logging.getLogger(__name__)

class RabbitMQClient:
    def __init__(self):
        self.host = os.getenv("RABBITMQ_HOST", "localhost")
        self.port = int(os.getenv("RABBITMQ_PORT", 5672))
        self.user = os.getenv("RABBITMQ_USER", "guest")
        self.password = os.getenv("RABBITMQ_PASSWORD", "guest")
        self.queue_name = "dinner.transactions"

    def get_connection(self):
        credentials = pika.PlainCredentials(self.user, self.password)
        parameters = pika.ConnectionParameters(
            host=self.host, 
            port=self.port, 
            credentials=credentials
        )
        return pika.BlockingConnection(parameters)

class RabbitMQPublisher(RabbitMQClient, MessagePublisher):
    def publish_transaction(self, transaction: Transaction) -> bool:
        try:
            connection = self.get_connection()
            channel = connection.channel()
            channel.queue_declare(queue=self.queue_name, durable=True)
            
            message = transaction.json()
            
            channel.basic_publish(
                exchange='',
                routing_key=self.queue_name,
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                )
            )
            logger.info(f"Published transaction for card {transaction.card_number}")
            connection.close()
            return True
        except Exception as e:
            logger.error(f"Failed to publish message: {str(e)}")
            return False
