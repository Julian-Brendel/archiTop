"""Sourcefile containing base_class for TableTop deck construction"""
from abc import ABC, abstractmethod
from typing import List

from data_types import Card

from config import load_config, getLogger

logger = getLogger(__name__)


# todo: add customization option
class DeckBuilder(ABC):
    """Abstract baseclass to construct TableTop deck assets"""

    current_card_id = 100
    current_card_asset_id = 1

    def __init__(self, cards: List[Card],
                 hidden=True,
                 custom_back=False):
        """Initializes deck builder with list of cards.

        Args:
            cards:      Cards to include in deck of cards
            hidden:     Determines if deck of cards is facing back up
                        Defaults to true
        """
        self.cards = cards
        self.hidden = hidden

        config = load_config()
        if custom_back:
            self.card_back_url = config['DECK']['CUSTOM_CARDBACK_URL']

        else:
            self.card_back_url = config['DECK']['DEFAULT_CARDBACK_URL']

    @abstractmethod
    def create_deck(self) -> dict:
        """Abstractmethod to be implemented by child class.
        Create the json structure for the deck of cards.

        Returns:
            TableTop card deck json structure
        """
        raise NotImplemented
