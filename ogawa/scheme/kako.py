import base64
from cerberus import Validator

# Cerberus compatible schema.
REQUEST_SCHEMA = {
    'ts': {'type': 'integer'},
    'cap': {'type': 'string'},
    'vuln': {'type': 'string'},
    'node': {'type': 'string'},
    'src_ip': {'type': 'string'},
    'src_port': {'type': 'integer'},
    'sim_name': {'type': 'string'},
    'sim_version': {'type': 'string'}
}


def validate(message):
    ''' Confirm the provided message matches the expected schema. '''
    v = Validator(REQUEST_SCHEMA)
    if not v.validate(message):
        raise AttributeError(v.errors)


def transform(message):
    ''' Apply any required transformations to input message. '''
    message['cap'] = base64.b64decode(message['cap'])
    if not message['cap']:
        message['cap'] = None

    return message
