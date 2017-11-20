# Ogawa

![Ogawa](docs/images/kako.png?raw=true)

This project provides multi-process ElasticSearch ingestion for SQS Queues.

 Ogawa will, by default, ensure that messages are in an acceptable format and can also perform transformation - such as encoding / decoding - before pushing into ElasticSearch. Although this project is intended for use in ingesting data output from tools such as Sesshu or Kako, additional schemes can be developed to ingest data from arbitrary sources.

## Dependencies

The following Python packages are required for Ogawa to function correctly:

* `click` - Command-line argument processing.
* `boto3` - Amazon AWS integration.
* `requests` - HTTP request library.
* `cerberus` - Validation of messages and other documents.

Once these modules are installed, a valid configuration file is required. See the **Configuration** section for more information.

## Configuration

The configuration for Ogawa is performed via a YAML document - named `ogawa.yaml` by default. An example configuration ships with Ogawa and is named `ogawa.dist.yaml`.

### AWS API

Currently, Ogawa assumes that `boto3` is able to enumerate credentials to access the configured SQS resources without intervention. This may be via `~/.aws/credentials` file, IAM Instance Profiles (recommended), environment variables, or otherwise. There is currently no ability to provide AWS access keys directly.

### Policies

The following provides an example IAM policy which can be used to create and grant a user access to retrieve messages from the relevant SQS queue - for use with Ogawa:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "sqs:DeleteMessage",
                "sqs:GetQueueUrl",
                "sqs:ReceiveMessage"
            ],
            "Resource": [
                "arn:aws:sqs:us-west-2:<ACCOUNT_NUMBER>:<SQS_QUEUE>"
            ]
        }
    ]
}
```

## Validation

By default, Ogawa will validate that the received message body matches the schema defined in the given scheme definition - `REQUEST_SCHEMA`. However, this can be disabled via the boolean configuration flag `bus.validation` inside of `ogawa.yaml`.

Be advised that in the event of a validation error, Ogawa will simply 'skip' the message and log the error without deleting it. This will cause the message to be re-queued after any applicable AWS SQS visibility timeout. In order to prevent perpetual receive loops due to validation errors a dead letter queue should be configured in SQS after a sane number of failed deliveries.

## Schemes

In order to allow for validation and transformation of application specific data, a `scheme` can be defined per acceptable input with relevant transformation and validation methods. These handlers will be invoked as part of regular Ogawa operation and ensure that application specific information is valid and transformed correctly.

The `scheme` to use is specified on the bus `input` as part of configuration. The value provided should match the name of the Python module which contains the relevant mappings.

See `ogawa/scheme/sample.py` for an example.

## ElasticSearch

As Ogawa is intended for use with writing data out to ElasticSearch, a sample index configuration for ElasticSearch - for handling Kako data - has been included below. This will need to be created on the target ElasticSearch instance, and customized to suit the scheme in use, and the required settings (such as shards, replication, etc).

```
cat <<KAKO_INDEX |
{
    "settings" : {
        "number_of_shards" : 1
    },
    "mappings": {
        "interaction": {
            "properties": {
                "capture": {"type": "text"},
                "vulnerability": {"type": "text"},
                "node": {"type": "text"},
                "destination_ip": {"type": "text"},
                "destination_port": {"type": "integer"},
                "source_ip": {"type": "text"},
                "source_port": {"type": "integer"},
                "simulation_name": {"type": "text"},
                "simulation_version": {"type": "string"},
                "timestamp": {
                    "type":   "date",
                    "format": "strict_date_optional_time||epoch_second"
                }
            }
        }
    }
}
KAKO_INDEX
curl -D - -X PUT -d @- http://127.0.0.1:9200/kako
```

## Additional Reading

A basic Chef environment cookbook for deploying and configuring Ogawa can be found at the following URL:

* https://www.github.com/darkarnium/om-env-ogawa/

Ogawa is designed to work with Sesshu and Kako which can be found at the following URL:

* https://www.github.com/darkarnium/sesshu/
* https://www.github.com/darkarnium/kako/
