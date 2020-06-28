"""Sourcefile containing functionality to load fetched card information from scryfall"""
import json
from functools import lru_cache
from pathlib import Path

from config import ROOT_PATH, getLogger, load_config
from .scryfall_fetcher import syncronize_scryfall_data


logger = getLogger(__name__)
conf = load_config()['SCRYFALL']


def _get_data_path():
    if scryfall_data := list(ROOT_PATH.glob(conf['BULK_DATA_FILE_PATTERN'])):
        return scryfall_data[0]


@lru_cache
def _load_scryfall_data(file_path: Path):
    logger.debug('Loading scryfall data')
    data = json.load(open(str(file_path), 'r'))
    return data


@lru_cache
def _load_scryfall_name_index(file_path: Path):
    data = _load_scryfall_data(file_path)
    return {entry['name']: entry for entry in data}


@lru_cache
def _load_scryfall_id_index(file_path: Path):
    data = _load_scryfall_data(file_path)
    return {entry['id']: entry for entry in data}


@lru_cache
def _load_scryfall_set_name_index(file_path: Path):
    data = _load_scryfall_data(file_path)
    index = {}
    for entry in data:
        index[entry['set']] = index.get(entry['set'], {})
        index[entry['set']][entry['name']] = entry
    return index


def load_scryfall_name_index():
    if _get_data_path() is None:
        logger.warning('No scryfall data present, downloading now')
        syncronize_scryfall_data()

    file_path = _get_data_path()
    return _load_scryfall_name_index(file_path)


def load_scryfall_id_index():
    if _get_data_path() is None:
        logger.warning('No scryfall data present, downloading now')
        syncronize_scryfall_data()

    file_path = _get_data_path()
    return _load_scryfall_id_index(file_path)


def load_scryfall_set_name_index():
    if _get_data_path() is None:
        logger.warning('No scryfall data present, downloading now')
        syncronize_scryfall_data()

    file_path = _get_data_path()
    return _load_scryfall_set_name_index(file_path)
