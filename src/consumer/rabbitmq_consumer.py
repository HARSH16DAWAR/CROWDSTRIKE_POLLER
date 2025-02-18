import pika
from ..config.settings import RABBITMQ_HOST, RABBITMQ_QUEUE
from .callback_handler import MessageHandler
from ..utils.logger import get_logger

logger = get_logger(__name__)

class RabbitMQConsumer:
    def __init__(self):
        self.host = RABBITMQ_HOST
        self.queue = RABBITMQ_QUEUE
        self.message_handler = MessageHandler()

    def start(self):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
            channel = connection.channel()
            
            channel.queue_declare(queue=self.queue, durable=True)
            channel.basic_qos(prefetch_count=1)
            
            channel.basic_consume(
                queue=self.queue,
                on_message_callback=self.message_handler.handle
            )
            
            logger.info("Consumer started. Waiting for messages...")
            channel.start_consuming()
            
        except Exception as e:
            logger.error(f"Consumer error: {str(e)}")
            raise
