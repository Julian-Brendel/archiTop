"""Sourcefile containing functionality to construct scryfall card deck"""
from functools import reduce
from typing import Dict, List, Tuple

from archiTop.data_types import RawCard, RawDeck
from archiTop.scryfall.data_types import ScryfallCard, ScryfallDeck
from archiTop.scryfall.scryfall_fetcher import syncronize_scryfall_data
from archiTop.scryfall.scryfall_loader import load_scryfall_id_index


class ScryfallDeckBuilder:

    def __init__(self, raw_deck: RawDeck, altered_cards_index: Dict[str, str]):
        syncronize_scryfall_data()

        # load index to search by name and scryfall id
        self.scryfall_id_index = load_scryfall_id_index()
        self.altered_cards_index = altered_cards_index
        self.raw_deck = raw_deck

    def construct_deck(self) -> ScryfallDeck:
        cards, tokens = self._get_scryfall_cards_for_deck()

        return ScryfallDeck(cards, tokens, self.raw_deck.name, self.raw_deck.thumbnail)

    def _get_scryfall_cards_for_deck(self) -> Tuple[List[ScryfallCard], List[ScryfallCard]]:
        mainboard = self.raw_deck.mainboard

        # convert raw cards to scryfall enriched cards
        scryfall_cards = [self._create_scryfall_card(card) for card in mainboard]

        # extract related cards for scryfall cards (token, etc.)
        related_cards = reduce(lambda set_1, set_2: set_1 | set_2,
                               [card.related_cards for card in scryfall_cards])
        return scryfall_cards, related_cards

    def _create_scryfall_card(self, card: RawCard) -> ScryfallCard:
        scryfall_data = self.scryfall_id_index[card.uid]
        altered_url = self.altered_cards_index.get(card.name)
        return ScryfallCard(scryfall_data,
                            quantity=card.quantity,
                            commander=card.commander,
                            altered_url=altered_url)
