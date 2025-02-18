from celery import Celery
from celery.schedules import crontab
from .rabbitmq_producer import RabbitMQProducer
from ..config.settings import CELERY_BROKER_URL
from ..utils.logger import get_logger

logger = get_logger(__name__)

app = Celery('tasks', broker=CELERY_BROKER_URL)

app.conf.beat_schedule = {
    'fetch-data-every-minute': {
        'task': 'src.producer.tasks.fetch_and_queue_data',
        'schedule': crontab(minute='*/1'),
    },
}

@app.task
def fetch_and_queue_data():
    producer = RabbitMQProducer()
    return producer.fetch_and_queue_data()
