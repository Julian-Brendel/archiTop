"""Sourcefile containing functionality to construct scryfall card deck"""
from functools import reduce
from typing import List, Tuple

from data_types import RawDeck
from .scryfall_loader import load_scryfall_name_index
from .data_types import ScryfallCard, ScryfallDeck


class ScryfallDeckBuilder:

    def __init__(self, raw_deck: RawDeck):
        # load index to search by name and scryfall id
        self.name_index = load_scryfall_name_index()
        self.raw_deck = raw_deck

    def construct_deck(self) -> ScryfallDeck:
        cards, tokens = self._get_scryfall_cards_for_deck()

        return ScryfallDeck(cards, tokens, self.raw_deck.name, self.raw_deck.thumbnail)

    def _get_scryfall_cards_for_deck(self) -> Tuple[List[ScryfallCard], List[ScryfallCard]]:
        mainboard = self.raw_deck.mainboard

        # convert raw cards to scryfall enriched cards
        scryfall_cards = [ScryfallCard(self.name_index[card.name],
                                       quantity=card.quantity,
                                       commander=card.commander) for card in mainboard]

        # extract related cards for scryfall cards (token, etc.)
        related_cards = reduce(lambda set1, set2: set1 | set2,
                               [card.related_cards for card in scryfall_cards])
        return scryfall_cards, related_cards
