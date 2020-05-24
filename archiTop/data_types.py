from copy import deepcopy
from dataclasses import dataclass
from typing import List


@dataclass
class Card:
    name: str
    image_url: str
    quantity: int

    def __repr__(self):
        return f'{self.quantity: <2} x {self.name}'

    def explode(self):
        new_self = deepcopy(self)
        new_self.quantity = 1

        return [new_self for _ in range(self.quantity)]


@dataclass
class Deck:
    mainboard: List[Card]
    name: str
    thumbnail: bytes
