"""Shared consumer logic for consumer.py, consumer_email.py and consumer_sms.py."""
import json
import sys
import time
from datetime import datetime, timezone

from bson import ObjectId
from bson.errors import InvalidId

from config import connect_db
from part2.models import EMAIL, Contact
from part2.rabbit import QUEUES, declare_queues, get_connection


def send_email(contact: Contact) -> bool:
    """Stub: pretend to send an email."""
    time.sleep(0.5)
    print(f"    email sent to {contact.email}")
    return True


def send_sms(contact: Contact) -> bool:
    """Stub: pretend to send an SMS."""
    time.sleep(0.5)
    print(f"    sms sent to {contact.phone}")
    return True



def process(body: bytes, method: str) -> None:
    try:
        contact_id = ObjectId(json.loads(body)["contact_id"])
    except (ValueError, KeyError, InvalidId):
        print(f"[!] Bad message: {body!r}")
        return

    contact = Contact.objects(id=contact_id).first()
    if contact is None:
        print(f"[!] Contact {contact_id} not found")
        return
    if contact.sent:
        print(f"[-] {contact.fullname}: already sent, skipped")
        return

    print(f"[x] {contact.fullname} via {method}")
    sender = send_email if method == EMAIL else send_sms
    if sender(contact):
        contact.update(sent=True, sent_at=datetime.now(timezone.utc))


def run(methods: list[str]) -> None:
    """Consume the queues of the given methods (email/sms) forever."""
    sys.stdout.reconfigure(encoding="utf-8")
    connect_db()
    connection = get_connection()
    channel = connection.channel()
    declare_queues(channel)
    channel.basic_qos(prefetch_count=1)

    for method_name in methods:
        def callback(ch, method, properties, body, _m=method_name):
            process(body, _m)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_consume(queue=QUEUES[method_name], on_message_callback=callback)

    queues = ", ".join(QUEUES[m] for m in methods)
    print(f"[*] Waiting for messages in {queues}. To exit press CTRL+C")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    finally:
        connection.close()
