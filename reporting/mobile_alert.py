# reporting/mobile_alert.py
"""Mobile alert utilities for RANZR."""

import os
from twilio.rest import Client
from config import settings

def send_mobile_alert(message_body: str) -> bool:
    """
    Sends an SMS mobile alert using Twilio.
    Requires 'twilio_account_sid', 'twilio_auth_token', 'twilio_from_number', 
    and 'twilio_to_number' in config/settings.yaml or as environment variables.
    """
    account_sid = settings.get("twilio_account_sid") or os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = settings.get("twilio_auth_token") or os.environ.get("TWILIO_AUTH_TOKEN")
    from_number = settings.get("twilio_from_number") or os.environ.get("TWILIO_FROM_NUMBER")
    to_number = settings.get("twilio_to_number") or os.environ.get("TWILIO_TO_NUMBER")

    if not all([account_sid, auth_token, from_number, to_number]):
        print(" -> Warning: Twilio credentials missing in config. Skipping true SMS mobile alert.")
        print(f" -> [Simulated Mobile Alert SMS]: {message_body}")
        return False

    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=message_body,
            from_=from_number,
            to=to_number
        )
        print(f" -> Mobile alert sent successfully. Message SID: {message.sid}")
        return True
    except Exception as e:
        print(f" -> Failed to send mobile alert: {e}")
        return False
