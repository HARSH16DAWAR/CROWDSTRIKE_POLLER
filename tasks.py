import requests
from celery import Celery
from celery.schedules import crontab
import pika
import json

# Initialize Celery
app = Celery('tasks', broker='amqp://localhost')

# Celery beat schedule configuration
app.conf.beat_schedule = {
    'fetch-data-every-minute': {  # Changed to every minute for testing
        'task': 'tasks.fetch_and_queue_data',
        'schedule': crontab(minute='*/1'),  # Every minute
    },
}

@app.task
def fetch_and_queue_data():
    try:
        # Make GET request to your Go endpoint
        response = requests.get('http://localhost:8080/data')
        data = response.json()
        
        # Connect to RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        
        # Declare queue
        channel.queue_declare(queue='mock_data_queue', durable=True)
        
        # Send data to queue
        channel.basic_publish(
            exchange='',
            routing_key='mock_data_queue',
            body=json.dumps(data),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
            )
        )
        
        connection.close()
        return f"Mock data fetched and queued successfully: {data}"
        
    except Exception as e:
        return f"Error occurred: {str(e)}"
