import pika
import json
import requests

def callback(ch, method, properties, body):
    try:
        # Parse the message
        data = json.loads(body)
        
        # Make POST request to your Go endpoint
        response = requests.post('http://localhost:8080/send-data', json=data)
        
        if response.status_code == 200:
            # Acknowledge the message
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print(f"Successfully posted mock data: {data}")
        else:
            # Negative acknowledgment - message will be requeued
            ch.basic_nack(delivery_tag=method.delivery_tag)
            print(f"Failed to post data. Status code: {response.status_code}")
            
    except Exception as e:
        # Negative acknowledgment in case of error
        ch.basic_nack(delivery_tag=method.delivery_tag)
        print(f"Error processing message: {str(e)}")

def start_consumer():
    # Connect to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    
    # Declare queue
    channel.queue_declare(queue='mock_data_queue', durable=True)
    
    # Set up consumer
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue='mock_data_queue',
        on_message_callback=callback
    )
    
    print("Mock data consumer started. Waiting for messages...")
    channel.start_consuming()

if __name__ == '__main__':
    start_consumer() 