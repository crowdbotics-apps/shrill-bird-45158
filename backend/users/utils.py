# utils.py
from twilio.rest import Client
from django.conf import settings

import random

def send_verification_code(user):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    verification_code = generate_verification_code()  # You need to implement this function
    user.verification_code = verification_code
    user.save()
    message = client.messages.create(
        body=f'Your verification code is: {verification_code}',
        from_=settings.TWILIO_PHONE_NUMBER,
        to=user.phone_number
    )
    return message


def generate_verification_code():
    # Generate a random 6-digit numeric code
    return ''.join(random.choices('0123456789', k=6))
