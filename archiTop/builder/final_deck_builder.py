"""Sourcefile containing final deck builder class for TableTop"""
import json
from copy import deepcopy
from typing import List

from builder.card_deck_builder import CardDeckBuilder
from data_types import Card, Deck
from resources import final_deck_template


class FinalDeckBuilder:
    final_deck_json = deepcopy(final_deck_template)

    card_decks = []

    def __init__(self, deck: Deck):
        self.deck = deck

    def construct_final_deck(self):

        # construct mainboard
        if mainboard_deck := self._construct_card_deck(self.deck.mainboard):
            self.card_decks.append(mainboard_deck)

        # construct token list
        if token_deck := None:
            self.card_decks.append(token_deck)

        # construct sideboard
        if sideboard_deck := None:
            self.card_decks.append(sideboard_deck)

        self.final_deck_json['ObjectStates'] = self.card_decks

    def save_deck(self):
        # save deck json
        json.dump(self.final_deck_json, open(f'{self.deck.name}.json', 'w'))
        # save deck thumbnail
        with open(f'{self.deck.name}.png', 'wb') as file:
            file.write(self.deck.thumbnail)

    @staticmethod
    def _construct_card_deck(card_list: List[Card]) -> dict:
        builder = CardDeckBuilder(card_list)
        return builder.create_deck()
