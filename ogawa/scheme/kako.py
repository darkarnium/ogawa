''' Implements a Kako scheme for Ogawa. '''

import re
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
        message['capture_text'] = None
        return message

    # Capture all printable characters and stash them inside a new field to
    # allow for easy searching inside of ES.
    candidate = re.findall("[\x00-\x7F]", decoded)
    if candidate:
        candidate = ''.join(candidate)
    else:
        candidate = None

    # Bolt on the plain-text capture and go!
    message['capture_txt'] = candidate
    return message
