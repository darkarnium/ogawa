from cerberus import Validator

# Define the request schema (for validation).
REQUEST_SCHEMA = {
    'plugin': {'type': 'string'},
    'target': {'type': 'string'}
}

# Define the response schema (for validation).
RESPONSE_SCHEMA = {
    'plugin': {'type': 'string'},
    'target': {'type': 'string'},
    'result': {'type': ['string', 'list', 'dict']}
}


def validate_request(message):
    ''' Test whether the provided request object is valid. '''
    v = Validator(REQUEST_SCHEMA)
    if not v.validate(message):
        raise AttributeError(v.errors)


def validate_response(message):
    ''' Tests whether the provided response object is valid. '''
    v = Validator(RESPONSE_SCHEMA)
    if not v.validate(message):
        raise AttributeError(v.errors)


def request():
    ''' Attempts to construct a request object. '''
    return None


def response(target, plugin, result):
    ''' Attempts to construct a response object. '''
    r = {
        'target': target,
        'plugin': plugin,
        'result': result
    }
    return r
