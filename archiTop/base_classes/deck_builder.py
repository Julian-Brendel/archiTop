from abc import ABC
from typing import List

from data_types import Card


class DeckBuilder(ABC):
    """Abstract baseclass to construct TableTop deck assets"""

    current_card_id = 100
    current_card_asset_id = 1

    card_back_url = 'https://www.frogtown.me/images/gatherer/CardBack.jpg'

    def __init__(self, cards: List[Card], hidden=True):
        self.cards = cards
        self.hidden = hidden

    def create_deck(self) -> dict:
        raise NotImplemented
