''' Implements configuration validation for Ogawa. '''

from cerberus import Validator

# Define the configuration schema (for validation).
SCHEMA = {
    'logging': {
        'type': 'dict',
        'schema': {
            'path': {'type': 'string'}
        }
    },
    'workers': {
        'type': 'dict',
        'schema': {
            'polling': {
                'type': 'dict',
                'schema': {
                    'interval': {'type': 'integer', 'min': 1, 'max': 20}
                }
            },
            'count': {'type': 'integer', 'min': 1}
        }
    },
    'monitoring': {
        'type': 'dict',
        'schema': {
            'enabled': {'type': 'boolean'},
            'interval': {'type': 'integer'}
        }
    },
    'bus': {
        'type': 'dict',
        'schema': {
            'region': {'type': 'string'},
            'validation': {'type': 'boolean'},
            'input': {
                'type': 'dict',
                'schema': {
                    'scheme': {'type': 'string'},
                    'queue': {'type': 'string'}
                }
            },
            'output': {
                'type': 'dict',
                'schema': {
                    'elasticsearch': {'type': 'string'}
                }
            }
        }
    }
}


def validate(config):
    ''' Test whether the provided configuration object is valid. '''
    linter = Validator(SCHEMA)
    if not linter.validate(config):
        raise AttributeError(linter.errors)
