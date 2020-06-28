from dataclasses import dataclass
from typing import List


@dataclass
class RawCard:
    """Class containing information for mtg card.
    One class instance can hold multiple quantities of a single card."""
    name: str                   # unique card name
    quantity: int               # quantity for card
    commander: bool = False     # flag whether card is commander


@dataclass
class RawDeck:
    """Class containing information for mtg deck of cards.
        This consists of the mainboard, sideboard and token / emblems."""
    mainboard: List[RawCard]  # list containing cards in mainboard
    name: str  # name of deck
    thumbnail: bytes  # image bytes for deck thumbnail
