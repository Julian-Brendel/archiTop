from dataclasses import dataclass
from copy import deepcopy


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
