"""Sourcefile containing functionality to fetch card information from scryfall"""
import pickle

import requests

from archiTop.scryfall import conf, logger, resources_path


def _extract_file_name(url: str) -> str:
    file_name = url.split('/')[-1]
    return file_name.replace('.json', '.pkl')


def get_bulk_url() -> str:
    request = requests.get(conf['BULK_META_URL']).json()
    oracle_cards = list(filter(lambda x: x['type'] == conf['BULK_DATA_IDENTIFIER'],
                               request['data']))[0]

    return oracle_cards['download_uri']


def update_scryfall_data(url: str):
    data = requests.get(url).json()
    pickle.dump(data, open(resources_path / _extract_file_name(url), 'wb'))


def syncronize_scryfall_data():
    current_url = get_bulk_url()
    file_name = _extract_file_name(current_url)
    print(file_name)
    if not (resources_path / file_name).exists():
        logger.info('Re-syncing scryfall data...')
        # delete outdated scryfall data
        for path in resources_path.glob(conf['BULK_DATA_FILE_PATTERN']):
            path.unlink()

        update_scryfall_data(current_url)

    logger.info('Scryfall data is up to date 🎉')
