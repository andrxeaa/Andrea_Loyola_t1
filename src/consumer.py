import json
import logging
from src.infrastructure.rabbitmq import RabbitMQClient
from src.infrastructure.repository import InMemoryCustomerRepository
from src.core.use_cases import CalculateRewardsUseCase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RewardConsumer(RabbitMQClient):
    def __init__(self):
        super().__init__()
        self.repository = InMemoryCustomerRepository()
        self.use_case = CalculateRewardsUseCase(self.repository)

    def callback(self, ch, method, properties, body):
        try:
            data = json.loads(body)
            logger.info(f"Received transaction: {data}")
            
            result = self.use_case.execute(data)
            logger.info(f"Reward calculated: Points={result.points_earned}, Cashback={result.cashback_earned}")
            
            account = self.repository.get_account(data['card_number'])
            logger.info(f"Account update: Total Points={account.total_points}, Total Cashback={account.total_cashback}")
            
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            # En caso de error, rechazamos y no reenviamos por ahora
            ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)

    def start_consuming(self):
        try:
            connection = self.get_connection()
            channel = connection.channel()
            channel.queue_declare(queue=self.queue_name, durable=True)
            
            # Procesar un mensaje a la vez
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback)
            
            logger.info('Waiting for messages. To exit press CTRL+C')
            channel.start_consuming()
        except Exception as e:
            logger.error(f"Failed to start consumer: {str(e)}")

if __name__ == '__main__':
    consumer = RewardConsumer()
    consumer.start_consuming()
