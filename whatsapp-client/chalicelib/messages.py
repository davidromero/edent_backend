from twilio.rest import Client
from chalicelib.config import TWILIO_SID, TWILIO_TOKEN

client = Client(TWILIO_SID, TWILIO_TOKEN)

def simple_message(body):
    from_num = 'whatsapp:+14155238886'
    to_num = f'whatsapp:+502{body["number"]}'
    client.messages.create(body=body["message"], from_=from_num, to=to_num)
    return
