from dataclasses import dataclass
from typing import List


@dataclass
class RawCard:
    """Class containing information for mtg card.
    One class instance can hold multiple quantities of a single card."""
    name: str                   # unique card name
    quantity: int               # quantity for card
    uid: str                    # unique card identifier
    editioncode: str = None     # edition code for card
    commander: bool = False     # flag whether card is commander

    def __repr__(self):
        return f'RawCard({self.quantity: <3}x {self.name} - {self.editioncode} - {self.uid})'


@dataclass
class RawDeck:
    """Class containing information for mtg deck of cards.
        This consists of the mainboard, sideboard and token / emblems."""
    mainboard: List[RawCard]  # list containing cards in mainboard
    name: str  # name of deck
    thumbnail: bytes  # image bytes for deck thumbnail

    def __repr__(self):
        total_cards = sum([card.quantity for card in self.mainboard])
        return f'RawDeck({total_cards} total cards, {len(self.mainboard)} unique cards)'
