# Ogawa

This project provides data retrieval support for Panorama. Currently, only Amazon SQS is supported for data input, and ElasticSearch for data output.

## Disclaimer

This code is so pre-alpha it hurts; expect problems! :fire:

## Dependencies

The following Python packages are required for Ogawa to function correctly:

* `click` - Command-line argument processing.
* `boto3` - Amazon AWS integration.
* `requests` - HTTP request library.
* `cerberus` - Validation of messages and other documents.

Once these modules are installed, a valid configuration file is required. See the **Configuration** section for more information.

## Configuration

The configuration for Ogawa is performed via a YAML document - named `ogawa.yaml` by default. An example configuration ships with Ogawa and is named `ogawa.dist.yaml`.

## Validation

By default, Ogawa will validate that the received message body matches the schema defined in `ogawa/config.py`. However, this can be disabled via the boolean configuration flag `bus.validation` inside of `ogawa.yaml`.

Be advised that in the event of a validation error, Ogawa will simply 'skip' the message and log the error without deleting it. This will cause the message to be re-queued after any applicable AWS SQS visibility timeout. In order to prevent perpetual receive loops due to validation errors, a dead letter queue should be configured in SQS after a sane number of failed deliveries.

### AWS API

Currently, Ogawa assumes that `boto3` is able to enumerate credentials to access the configured SNS and SQS resources without intervention. This may be via `~/.aws/credentials` file, IAM Instance Profiles (recommended), environment variables, or otherwise. This is done to encourage the use of IAM Instance Profiles, rather than generating AWS access keys and placing them into unencrypted text files.

There is currently no ability to provide AWS access keys directly.

## Schemes

In order to allow for validation and transformation of application specific data, a `scheme` can be defined per acceptable input with relevant transformation and validation methods. These handlers will be invoked as part of regular Ogawa operation and ensure that application specific information is valid and transformed correctly.

The `scheme` to use is specified on the bus `input` as part of configuration. The value provided should match the name of the Python module which contains the relevant mappings.

See `ogawa/scheme/kako.py` for an example.

## Additional Reading

A basic Chef environment cookbook for deploying and configuring Ogawa can be found at the following URL:

* https://www.github.com/darkarnium/ogawa-env/

Ogawa is designed to work with Sesshu, which can be found at the following URL:

* https://www.github.com/darkarnium/sesshu/
