"""Sourcefile containing functionality to load fetched card information from scryfall"""
import pickle
from functools import lru_cache
from pathlib import Path

from archiTop.scryfall import conf, spin_logger, resources_path


def _get_data_path() -> Path:
    if scryfall_data := list(resources_path.glob(conf['BULK_DATA_FILE_PATTERN'])):
        return scryfall_data[0]


@lru_cache
def _load_scryfall_data(file_path: Path):
    spin_logger.debug('Loading scryfall data', extra={'user_waiting': True})
    data = pickle.load(file_path.open('rb'))
    spin_logger.debug('Loaded scryfall data', extra={'user_waiting': False})
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
    file_path = _get_data_path()
    return _load_scryfall_name_index(file_path)


def load_scryfall_id_index():
    file_path = _get_data_path()
    return _load_scryfall_id_index(file_path)


def load_scryfall_set_name_index():
    file_path = _get_data_path()
    return _load_scryfall_set_name_index(file_path)
