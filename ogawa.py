#!/usr/bin/env python

import os
import yaml
import click
import logging
import logging.config

import multiprocessing

from ogawa import worker
from ogawa import config
from ogawa import constant


@click.command()
@click.option('--configuration-file', help='Path to YAML configuration file.')
def main(configuration_file):
    ''' Panorama Ogawa. '''

    # Determine the configuration file to use.
    if configuration_file is None:
        configuration_file = os.path.join(
            os.path.dirname(__file__), constant.DEFAULT_CONFIGURATION_FILE
        )
    else:
        configuration_file = os.path.join(
            os.path.abspath(configuration_file)
        )

    # Read in the application configuration.
    with open(configuration_file, 'r') as f:
        configuration = yaml.safe_load(f.read())
        config.validate(configuration)

    # Configure the logger.
    log_path = os.path.join(
        configuration['logging']['path'], '{}.log'.format(
            configuration['logging']['name']
        )
    )
    logging.basicConfig(
        level=logging.INFO,
        format='[%(process)d] - %(asctime)s - %(levelname)s - %(message)s',
        filename=log_path
    )

    # Grab a logger.
    log = logging.getLogger(configuration['logging']['name'])

    # Spawn N workers - per configuration.
    log.info('Spawning {} workers'.format(configuration['workers']['count']))
    for i in xrange(configuration['workers']['count']):
        p = multiprocessing.Process(target=worker.run, args=(configuration,))
        p.start()

    # TODO: Monitor children and heartbeat to registry.
    log.info('All workers created successfully.')

if __name__ == '__main__':
    main()
