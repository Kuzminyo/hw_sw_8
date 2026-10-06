import pika

from config import RABBITMQ_HOST, RABBITMQ_PASSWORD, RABBITMQ_PORT, RABBITMQ_USER
from part2.models import EMAIL, SMS

QUEUES = {EMAIL: "email_queue", SMS: "sms_queue"}


def get_connection() -> pika.BlockingConnection:
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    params = pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials)
    return pika.BlockingConnection(params)


def declare_queues(channel) -> None:
    for queue in QUEUES.values():
        channel.queue_declare(queue=queue, durable=True)
