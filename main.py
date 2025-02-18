from src.consumer.rabbitmq_consumer import RabbitMQConsumer

def main():
    consumer = RabbitMQConsumer()
    consumer.start()

if __name__ == '__main__':
    main()
