import configparser
import logging
from pathlib import Path


def load_config():
    """Creates config-parser, reading the config and returning the read config

    Returns:
        Parsed config
    """
    config = configparser.ConfigParser()
    config.read(PACKAGE_ROOT_PATH / 'config.ini')
    return config


def setup_logging():
    logger = logging.getLogger('archiTop')
    logger.setLevel(load_config()['APP']['LOG_LEVEL'])
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Attach stdout handler to logger (log to console)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def getLogger(name: str):
    return logging.getLogger('archiTop.' + name)


PACKAGE_ROOT_PATH = Path(__file__).parent
setup_logging()
