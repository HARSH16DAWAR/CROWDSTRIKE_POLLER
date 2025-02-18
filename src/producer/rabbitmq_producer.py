import json
import pika
import requests
from ..config.settings import RABBITMQ_HOST, RABBITMQ_QUEUE, API_BASE_URL, API_ENDPOINTS
from ..utils.logger import get_logger

logger = get_logger(__name__)

class RabbitMQProducer:
    def __init__(self):
        self.host = RABBITMQ_HOST
        self.queue = RABBITMQ_QUEUE

    def _get_channel(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
        channel = connection.channel()
        channel.queue_declare(queue=self.queue, durable=True)
        return connection, channel

    def fetch_and_queue_data(self):
        try:
            # Fetch data from API
            response = requests.get(f"{API_BASE_URL}{API_ENDPOINTS['get_data']}")
            data = response.json()
            
            # Setup RabbitMQ connection and channel
            connection, channel = self._get_channel()
            
            # Publish message
            channel.basic_publish(
                exchange='',
                routing_key=self.queue,
                body=json.dumps(data),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Make message persistent
                )
            )
            
            connection.close()
            logger.info(f"Successfully fetched and queued data: {data}")
            return f"Data fetched and queued successfully: {data}"
            
        except requests.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error in fetch_and_queue_data: {str(e)}")
            raise
