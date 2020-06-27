import configparser
import logging
from pathlib import Path


def find_root_path() -> Path:
    """Finds root path of project by searching for the `src` folder recursively in the parent
    directories

    Returns:
        Path to root of project directory
    """

    path = Path(Path.cwd(), "dummy")
    while path != path.parent:
        src_path = Path(path, "archiTop")
        if src_path.exists():
            return path
        path = path.parent


def load_config():
    """Creates config-parser, reading the config and returning the read config

    Returns:
        Parsed config
    """
    config = configparser.ConfigParser()
    config.read(Path(ROOT_PATH, 'archiTop', 'config.ini'))
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


ROOT_PATH = find_root_path()
setup_logging()
