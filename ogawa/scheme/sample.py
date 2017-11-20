''' Implements an Example / Sample scheme for Ogawa. '''

from cerberus import Validator

# Cerberus compatible schema.
REQUEST_SCHEMA = {
    'key': {'type': 'string'},
    'value': {'type': 'string'}
}


def validate(message):
    ''' Confirm the provided message matches the expected schema. '''
    linter = Validator(REQUEST_SCHEMA)
    if not linter.validate(message):
        raise AttributeError(linter.errors)


def transform(message):
    ''' Apply any required transformations to input message. '''
    return message
