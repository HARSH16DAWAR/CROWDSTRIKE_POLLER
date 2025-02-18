import json
import requests
from ..config.settings import API_BASE_URL, API_ENDPOINTS
from ..utils.logger import get_logger

logger = get_logger(__name__)

class MessageHandler:
    def handle(self, ch, method, properties, body):
        try:
            data = json.loads(body)
            response = requests.post(
                f"{API_BASE_URL}{API_ENDPOINTS['send_data']}", 
                json=data
            )
            
            if response.status_code == 200:
                ch.basic_ack(delivery_tag=method.delivery_tag)
                logger.info(f"Successfully processed data: {data}")
            else:
                ch.basic_nack(delivery_tag=method.delivery_tag)
                logger.error(f"Failed to process data. Status: {response.status_code}")
                
        except Exception as e:
            ch.basic_nack(delivery_tag=method.delivery_tag)
            logger.error(f"Error processing message: {str(e)}")
