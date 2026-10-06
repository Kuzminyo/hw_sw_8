"""Process contacts from sms_queue.

Run from the project root:  python -m part2.consumer_sms
"""
from part2.models import SMS
from part2.worker import run

if __name__ == "__main__":
    run([SMS])
