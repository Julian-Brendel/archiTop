import configparser
import logging
from pathlib import Path

from logging_spinner import SpinnerHandler


def load_config():
    """Creates config-parser, reading the config and returning the read config

    Returns:
        Parsed config
    """
    config = configparser.ConfigParser()
    config.read(PACKAGE_ROOT_PATH / 'config.ini')
    return config


def setup_spin_logging():
    logger = logging.getLogger('archiTop_spin')
    logger.setLevel(load_config()['APP']['LOG_LEVEL'])
    logger.addHandler(SpinnerHandler())


def get_spin_logger(name: str):
    return logging.getLogger('archiTop_spin.' + name)


PACKAGE_ROOT_PATH = Path(__file__).parent
setup_spin_logging()
