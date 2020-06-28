"""Sourcefile containing functionality to fetch card information from scryfall"""
import json
from pathlib import Path

import requests

from config import ROOT_PATH, getLogger, load_config


logger = getLogger(__name__)
conf = load_config()['SCRYFALL']


def _extract_file_name(url: str) -> str:
    return url.split('/')[-1]


def get_bulk_url() -> str:
    request = requests.get(conf['BULK_META_URL']).json()
    oracle_cards = list(filter(lambda x: x['type'] == conf['BULK_DATA_IDENTIFIER'],
                               request['data']))[0]

    return oracle_cards['download_uri']


def update_scryfall_data(url: str):
    data = requests.get(url).json()
    json.dump(data, open(Path(ROOT_PATH, _extract_file_name(url)), 'w'))


def syncronize_scryfall_data():
    current_url = get_bulk_url()
    file_name = _extract_file_name(current_url)
    if not Path(ROOT_PATH, file_name).exists():
        logger.info('Re-syncing scryfall data...')
        # delete outdated scryfall data
        for path in ROOT_PATH.glob(conf['BULK_DATA_FILE_PATTERN']):
            path.unlink()

        update_scryfall_data(current_url)

    logger.info('Scryfall data is up to date 🎉')
