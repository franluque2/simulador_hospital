from secret_keys import WHATSAPP_KEY, WHATSAPP_ID, WHATSAPP_SENDER

from twilio.rest import Client

account_sid = WHATSAPP_ID
auth_token = WHATSAPP_KEY
account_sender= WHATSAPP_SENDER
client = Client(account_sid, auth_token)

def sendWhatsAppMessage(messagebody: str, number: int) -> bool:
    message = client.messages.create(
    from_=account_sender,
    body=messagebody,
    to=f'whatsapp:+{number}'
    )
    return message.status!="failed"
