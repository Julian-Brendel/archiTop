"""Sourcefile containing final deck builder class for TableTop"""
import json
from copy import deepcopy
from typing import List

from builder.card_deck_builder import CardDeckBuilder
from data_types import Card
from resources import final_deck_template


class FinalDeckBuilder:
    final_deck_json = deepcopy(final_deck_template)

    card_decks = []

    def __init__(self, deck_name, *card_lists: List[Card]):
        self.deck_name = deck_name
        self.card_lists = card_lists

    def construct_final_deck(self):
        for card_list in self.card_lists:
            self.card_decks.append(self._construct_card_deck(card_list))

        self.final_deck_json['ObjectStates'] = self.card_decks

    def save_deck(self):
        json.dump(self.final_deck_json, open(f'{self.deck_name}.json', 'w'))

    @staticmethod
    def _construct_card_deck(card_list: List[Card]) -> dict:
        builder = CardDeckBuilder(card_list)
        return builder.create_deck()
