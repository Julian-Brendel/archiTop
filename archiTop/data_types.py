from dataclasses import dataclass
from functools import reduce
from typing import List


@dataclass
class Card:
    """Class containing information for mtg card.
    One class instance can hold multiple quantities of a single card."""
    name: str                   # unique card name
    image_url: str              # card image url
    quantity: int               # quantity for card
    commander: bool             # flag whether card is commander

    def __repr__(self):
        return f'Card({self.quantity: <2} x {self.name})'


# todo: add support for sideboard
# todo: add support for token / misc
@dataclass
class Deck:
    """Class containing information for mtg deck of cards.
    This consists of the mainboard, sideboard and token / emblems."""
    mainboard: List[Card]       # list containing cards in mainboard
    name: str                   # name of deck
    thumbnail: bytes            # image bytes for deck thumbnail

    def __repr__(self):
        total_count = reduce(lambda a, b: a + b.quantity, self.mainboard, 0)
        return f'Deck[{self.name}]({total_count} total cards, {len(self.mainboard)} unique cards))'
