''' Ogawa - ElasticSearch ingestion for SQS Queues. '''

import os
import time
import logging
import logging.config
import multiprocessing
import yaml
import click

import ogawa


def spawn_worker(configuration=None):
    ''' Attempts to spawn a worker, returning the process. '''
    process = multiprocessing.Process(
        target=ogawa.worker.run, args=(configuration,)
    )
    process.start()
    return process


@click.command()
@click.option('--configuration-file', help='Path to YAML configuration file.')
def main(configuration_file):
    ''' Ogawa - ElasticSearch ingestion for SQS Queues. '''

    # Determine the configuration file to use.
    if configuration_file is None:
        configuration_file = os.path.join(
            os.path.dirname(__file__), ogawa.constant.DEFAULT_CONFIGURATION_FILE
        )
    else:
        configuration_file = os.path.join(
            os.path.abspath(configuration_file)
        )

    # Read in the application configuration.
    with open(configuration_file, 'r') as hndl:
        configuration = yaml.safe_load(hndl.read())
        ogawa.config.validate(configuration)

    # Configure the logger.
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(process)d - [%(levelname)s] %(message)s',
        filename=os.path.join(configuration['logging']['path'], 'ogawa.log')
    )
    log = logging.getLogger(__name__)

    # Bring down the logger level(s) for boto to prevent log spam during AWS
    # operations - such as pushing messages to SNS.
    logging.getLogger('boto3').setLevel(logging.WARNING)
    logging.getLogger('botocore').setLevel(logging.WARNING)

    # Spawn N workers - per configuration.
    workers = dict()
    log.info('Spawning %d workers', configuration['workers']['count'])
    for idx in xrange(configuration['workers']['count']):
        workers[idx] = spawn_worker(configuration)

    # Start monitoring loop.
    if configuration['monitoring']['enabled']:
        log.info(
            'Monitoring enabled every %s seconds',
            configuration['monitoring']['interval']
        )
        while True:
            for idx, process in workers.iteritems():
                if not process.is_alive():
                    log.error('worker %d has died, respawning', idx)
                    workers[idx] = spawn_worker(configuration)

            # ...and wait.
            log.debug('Monitor run complete, sleeping before next run.')
            time.sleep(configuration['monitoring']['interval'])

if __name__ == '__main__':
    main()
