''' Implements a Kako scheme for Ogawa. '''

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
    linter = Validator(REQUEST_SCHEMA)
    if not linter.validate(message):
        raise AttributeError(linter.errors)


def transform(message):
    ''' Apply any required transformations to input message. '''
    try:
        decoded = base64.b64decode(message['capture'])
    except TypeError as _:
        return message

    # Encode non-printable characters.
    candidate = ''
    for char in decoded:
        candidate += char

    # This seems odd, but we're replacing an empty string with None explicitly
    # to prevent empty captures being recorded in ES.
    if candidate is None:
        message['capture'] = None
    else:
        message['capture'] = candidate

    return message
