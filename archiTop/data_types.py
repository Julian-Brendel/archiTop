from copy import deepcopy
from dataclasses import dataclass
from functools import reduce
from typing import List


@dataclass
class Card:
    name: str
    image_url: str
    quantity: int
    commander: bool

    def __repr__(self):
        return f'Card({self.quantity: <2} x {self.name})'


@dataclass
class Deck:
    mainboard: List[Card]
    name: str
    thumbnail: bytes

    def __repr__(self):
        total_count = reduce(lambda a, b: a + b.quantity, self.mainboard, 0)
        return f'Deck[{self.name}]({total_count} total cards, {len(self.mainboard)} unique cards))'
