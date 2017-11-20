import base64
from cerberus import Validator

# Cerberus compatible schema.
REQUEST_SCHEMA = {
    'timestamp': {'type': 'integer'},
    'capture': {'type': 'string'},
    'vulnerability': {'type': 'string'},
    'node': {'type': 'string'},
    'destination_ip': {'type': 'string'},
    'destination_port': {'type': 'integer'},
    'source_ip': {'type': 'string'},
    'source_port': {'type': 'integer'},
    'simulation_name': {'type': 'string'},
    'simulation_version': {'type': 'string'}
}


def validate(message):
    ''' Confirm the provided message matches the expected schema. '''
    v = Validator(REQUEST_SCHEMA)
    if not v.validate(message):
        raise AttributeError(v.errors)


def transform(message):
    ''' Apply any required transformations to input message. '''
    message['capture'] = base64.b64decode(message['capture'])
    if not message['capture']:
        message['capture'] = None

    return message
