"""Process all contacts from both queues (email and sms).

Run from the project root:  python -m part2.consumer
"""
from part2.models import EMAIL, SMS
from part2.worker import run

if __name__ == "__main__":
    run([EMAIL, SMS])
