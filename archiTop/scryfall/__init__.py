from pathlib import Path

from archiTop.config import PACKAGE_ROOT_PATH, get_spin_logger, load_config

spin_logger = get_spin_logger(__name__)
conf = load_config()['SCRYFALL']
resources_path = Path(PACKAGE_ROOT_PATH, 'resources')

from .scryfall_builder import ScryfallDeckBuilder
from .scryfall_fetcher import syncronize_scryfall_data, syncronize_scryfall_data
from .scryfall_loader import load_scryfall_id_index
