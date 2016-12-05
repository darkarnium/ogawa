from cerberus import Validator

# Define the configuration schema (for validation).
SCHEMA = {
    'logging': {
        'type': 'dict',
        'schema': {
            'path': {'type': 'string'},
            'name': {'type': 'string'}
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
    'bus': {
        'type': 'dict',
        'schema': {
            'region': {'type': 'string'},
            'input': {
                'type': 'dict',
                'schema': {
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
    v = Validator(SCHEMA)
    if not v.validate(config):
        raise AttributeError(v.errors)
