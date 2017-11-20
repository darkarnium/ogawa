''' Implements the primary Ogawa ingestion worker. '''

import logging
import json
import boto3
import requests

from ogawa import config
from ogawa import scheme


def run(configuration):
    ''' Long-polls messages from the queue and records them. '''
    config.validate(configuration)
    log = logging.getLogger(configuration['logging']['name'])

    # Ensure the configured scheme handler exists.
    try:
        scheme_handle = getattr(scheme, configuration['bus']['input']['scheme'])
    except AttributeError as err:
        log.error(
            'Unable to load configured scheme handler %s: %s',
            configuration['bus']['input']['scheme'], err
        )
        raise

    # Setup SQS poller and poll until the heat death of the universe. Or,
    # y'know, until we crash / stop / restart.
    sqs = boto3.client('sqs', region_name=configuration['bus']['region'])
    log.info(
        'Starting long-poll loop for messages from %s',
        configuration['bus']['input']['queue']
    )

    while True:
        queue = sqs.receive_message(
            QueueUrl=configuration['bus']['input']['queue'],
            WaitTimeSeconds=configuration['workers']['polling']['interval']
        )

        try:
            messages = queue['Messages']
        except KeyError:
            log.info('No messages in queue, re-polling')
            continue

        # Iterate over polled messages, validate objects, and dispatch to the
        # relevant module.
        log.info('Got %d messages from the queue', len(messages))
        for i in xrange(0, len(messages)):
            mid = messages[i]['MessageId']
            handle = messages[i]['ReceiptHandle']

            # The 'Body' is JSON and contains a 'Message' that is also JSON.
            log.info('[%s] Processing message body', mid)
            try:
                body = json.loads(messages[i]['Body'])
                work = json.loads(body['Message'])

                # Validate the extracted message.
                if configuration['bus']['validation']:
                    scheme_handle.validate(work)
            except (ValueError, AttributeError) as err:
                log.warn('[%s] skipping malformed message: %s', mid, err)
                continue

            # Apply transformations.
            work = scheme_handle.transform(work)

            # Dispatch the result into ElasticSearch.
            try:
                _ = requests.post(
                    configuration['bus']['output']['elasticsearch'],
                    json=work
                )
            except UnicodeDecodeError as err:
                log.error('[%s] Failed to encode capture: %s', mid, err)
                continue
            except requests.exceptions.HTTPError as err:
                log.error('[%s] Failed to POST to ElasticSearch: %s', mid, err)
                continue

            # Delete.
            log.info('[%s] Message processed successfully', mid)
            sqs.delete_message(
                QueueUrl=configuration['bus']['input']['queue'],
                ReceiptHandle=handle
            )
