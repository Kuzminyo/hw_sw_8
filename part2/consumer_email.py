"""Process contacts from email_queue.

Run from the project root:  python -m part2.consumer_email
"""
from part2.models import EMAIL
from part2.worker import run

if __name__ == "__main__":
    run([EMAIL])
