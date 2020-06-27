"""Sourcefile fetching card information from scryfall"""
import json
from pathlib import Path

import requests

from config import ROOT_PATH, getLogger


logger = getLogger(__name__)


def _extract_file_name(url: str) -> str:
    return url.split('/')[-1]


def get_bulk_url() -> str:
    request = requests.get('https://api.scryfall.com/bulk-data').json()
    oracle_cards = list(filter(lambda x: x['type'] == 'oracle_cards', request['data']))[0]

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
        for path in ROOT_PATH.glob('oracle-cards*.json'):
            path.unlink()

        update_scryfall_data(current_url)

    logger.info('Scryfall data is up to date 🎉')
