from datetime import datetime, timezone

from mongoengine import BooleanField, DateTimeField, Document, EmailField, StringField

EMAIL = "email"
SMS = "sms"


class Contact(Document):
    fullname = StringField(required=True)
    email = EmailField(required=True)
    phone = StringField(required=True)
    preferred_method = StringField(choices=(EMAIL, SMS), default=EMAIL)
    address = StringField()
    company = StringField()
    sent = BooleanField(default=False)
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    sent_at = DateTimeField()

    meta = {"collection": "contacts"}
