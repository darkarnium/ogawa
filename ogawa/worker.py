import json
import boto3
import logging
import requests

from ogawa import config
from ogawa import constant
from ogawa import message


def run(configuration):
    ''' Long-polls messages from the queue and records them. '''
    config.validate(configuration)

    log = logging.getLogger(configuration['logging']['name'])
    sqs = boto3.client('sqs', region_name=configuration['bus']['region'])

    # Poll until the heat death of the universe.
    log.info(
        'Starting long-poll loop for messages from {}'.format(
            configuration['bus']['input']['queue']
        )
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
        log.info('Got {} messages from the queue'.format(len(messages)))
        for i in xrange(0, len(messages)):
            mid = messages[i]['MessageId']
            handle = messages[i]['ReceiptHandle']

            # 'Body' is JSON, which contains 'Message' which is also JSON.
            log.info('[{}] Processing message body'.format(mid))
            try:
                body = json.loads(messages[i]['Body'])
                work = json.loads(body['Message'])

                # Validate the message, if configured.
                if configuration['bus']['validation']:
                    message.validate_response(work)
            except (ValueError, AttributeError) as e:
                log.warn('[{}] skipping malformed message: {}'.format(mid, e))
                continue

            # Dispatch the result into ElasticSearch.
            try:
                result = requests.post(
                    configuration['bus']['output']['elasticsearch'],
                    json=work
                )
            except requests.exceptions.HTTPError as x:
                log.error(
                    '[{}] Failed to POST to ElasticSearch: {}'.format(mid, x)
                )
                continue

            # Delete.
            log.info('[{}] Message processed successfully'.format(mid))
            sqs.delete_message(
                QueueUrl=configuration['bus']['input']['queue'],
                ReceiptHandle=handle
            )
