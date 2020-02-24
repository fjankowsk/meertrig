#
#   2020 Fabian Jankowski
#   Configuration file related helper functions.
#

import logging
import os.path

import yaml


def get_config():
    """
    Load and parse a config file.

    Returns
    -------
    config: dict
        Dictionary with configuration.

    Raises
    ------
    RuntimeError
        If `filename` does not exist.
    """

    filename = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yml')
    filename = os.path.abspath(filename)

    log = logging.getLogger('meertrig.config_helpers')
    log.debug('Configuration file: {0}'.format(filename))

    if not os.path.isfile(filename):
        raise RuntimeError('Config file does not exist: {0}'.format(filename))
    
    with open(filename, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    return config
