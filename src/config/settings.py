from dotenv import load_dotenv
import os

load_dotenv()

# RabbitMQ Configuration
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE', 'mock_data_queue')

# API Configuration
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8080')
API_ENDPOINTS = {
    'send_data': '/send-data',
    'get_data': '/data'
}

# Celery Configuration
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'amqp://localhost')
