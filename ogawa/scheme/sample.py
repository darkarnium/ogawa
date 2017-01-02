from cerberus import Validator

# Cerberus compatible schema.
REQUEST_SCHEMA = {
    'key': {'type': 'string'},
    'value': {'type': 'string'}
}


def validate(message):
    ''' Confirm the provided message matches the expected schema. '''
    v = Validator(REQUEST_SCHEMA)
    if not v.validate(message):
        raise AttributeError(v.errors)


def transform(message):
    ''' Apply any required transformations to input message. '''
    return message
