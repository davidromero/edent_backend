from chalice import Chalice
from chalicelib import messages, custom_responses, config

app = Chalice(app_name='whatsapp-client')


@app.route('/')
def index():
    return custom_responses.get_base_res()


@app.route('/message', methods=['POST'], cors=config.cors_config)
def add_new_patient():
    body = app.current_request.json_body
    status = messages.simple_message(body)
    return f'Message sent'