"""Sourcefile containing functionality to construct scryfall card deck"""
from functools import reduce
from typing import List, Tuple

from archiTop.data_types import RawCard, RawDeck
from archiTop.scryfall.data_types import ScryfallCard, ScryfallDeck
from archiTop.scryfall.scryfall_fetcher import syncronize_scryfall_data
from archiTop.scryfall.scryfall_loader import (load_scryfall_name_index,
                                               load_scryfall_set_name_index)


class ScryfallDeckBuilder:

    def __init__(self, raw_deck: RawDeck):
        syncronize_scryfall_data()

        # load index to search by name and scryfall id
        self.name_index = load_scryfall_name_index()
        self.set_name_index = load_scryfall_set_name_index()
        self.raw_deck = raw_deck

    def construct_deck(self) -> ScryfallDeck:
        cards, tokens = self._get_scryfall_cards_for_deck()

        return ScryfallDeck(cards, tokens, self.raw_deck.name, self.raw_deck.thumbnail)

    def _get_scryfall_cards_for_deck(self) -> Tuple[List[ScryfallCard], List[ScryfallCard]]:
        mainboard = self.raw_deck.mainboard

        # convert raw cards to scryfall enriched cards
        scryfall_cards = [self._create_scryfall_card(card) for card in mainboard]

        # extract related cards for scryfall cards (token, etc.)
        related_cards = reduce(lambda set1, set2: set1 | set2,
                               [card.related_cards for card in scryfall_cards])
        return scryfall_cards, related_cards

    def _create_scryfall_card(self, card: RawCard) -> ScryfallCard:
        if card.editioncode is not None:
            scryfall_data = self.set_name_index[card.editioncode][card.name]
        else:
            scryfall_data = self.name_index[card.name]
        return ScryfallCard(scryfall_data,
                            quantity=card.quantity,
                            commander=card.commander)
