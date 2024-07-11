from time import sleep

from celery import Celery
from fastapi import APIRouter

from src.config import settings

broker_url = "amqp://{0}:{1}@rabbit_mq:{2}".format(
    settings.RABBITMQ_DEFAULT_USER, settings.RABBITMQ_DEFAULT_PASS, settings.RABBITMQ_PORT
)

app = Celery("celery-router", broker=broker_url)


@app.task
def test():
    sleep(15)
    return "200"
