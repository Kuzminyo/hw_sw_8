"""Generate fake contacts, save them to MongoDB and queue their ids.

Run from the project root:  python -m part2.producer [count]
Each contact goes to the queue of its preferred method: email_queue or sms_queue.
"""
import json
import random
import sys

import pika
from faker import Faker

from config import connect_db
from part2.models import EMAIL, SMS, Contact
from part2.rabbit import QUEUES, declare_queues, get_connection

fake = Faker("uk_UA")


def create_contact() -> Contact:
    return Contact(
        fullname=fake.name(),
        email=fake.email(),
        phone=fake.phone_number(),
        preferred_method=random.choice((EMAIL, SMS)),
        address=fake.address(),
        company=fake.company(),
    ).save()


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    connect_db()
    connection = get_connection()
    channel = connection.channel()
    declare_queues(channel)

    for _ in range(count):
        contact = create_contact()
        queue = QUEUES[contact.preferred_method]
        channel.basic_publish(
            exchange="",
            routing_key=queue,
            body=json.dumps({"contact_id": str(contact.id)}).encode(),
            properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
        )
        print(f"[x] {queue}: {contact.id} {contact.fullname}")

    connection.close()
    print(f"Queued {count} contacts.")


if __name__ == "__main__":
    main()
