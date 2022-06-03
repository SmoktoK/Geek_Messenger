import json
from Messenger.decos import log
from Messenger.common.variables import MAX_PACKAGE_LENGTH, ENCODING

@log
def get_message(client):
    encoded = client.recv(MAX_PACKAGE_LENGTH)
    if isinstance(encoded, bytes):
        json_response = encoded.decode(ENCODING)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError

@log
def send_message(sock, message):
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock.send(encoded_message)
