"""Sourcefile containing final deck builder class for TableTop"""
import json
from copy import deepcopy
from typing import List, Optional

from builder.multi_card_deck_builder import MultiCardDeckBuilder
from builder.single_card_deck_builder import SingleCardDeckBuilder
from data_types import Card, Deck
from resources import final_deck_template


class DeckBuilderWrapper:
    final_deck_json = deepcopy(final_deck_template)

    card_decks = []

    def __init__(self, deck: Deck):
        self.deck = deck

    def construct_final_deck(self):

        mainboard_cards = list(filter(lambda card: not card.commander, self.deck.mainboard))
        commander_cards = list(filter(lambda card: card.commander, self.deck.mainboard))

        # construct mainboard
        if mainboard_deck := self._construct_card_deck(mainboard_cards):
            self.card_decks.append(mainboard_deck)

        if commander_deck := self._construct_card_deck(commander_cards, hidden=False):
            self.card_decks.append(commander_deck)

        # construct token list
        if token_deck := None:
            self.card_decks.append(token_deck)

        # construct sideboard
        if sideboard_deck := None:
            self.card_decks.append(sideboard_deck)

        # shift deck positions so piles do not combine
        current_x_pos = 0
        for deck in self.card_decks:
            deck['Transform']['posX'] = current_x_pos
            current_x_pos += 2.2

        self.final_deck_json['ObjectStates'] = self.card_decks

    def save_deck(self):
        # save deck json
        json.dump(self.final_deck_json, open(f'{self.deck.name}.json', 'w'))
        # save deck thumbnail
        with open(f'{self.deck.name}.png', 'wb') as file:
            file.write(self.deck.thumbnail)

    @staticmethod
    def _construct_card_deck(card_list: List[Card], hidden=True) -> Optional[dict]:
        if len(card_list) > 1:
            builder = MultiCardDeckBuilder(card_list, hidden)
        elif len(card_list) == 1:
            builder = SingleCardDeckBuilder(card_list, hidden)
        else:
            print('passed card list is empty')
            return None

        return builder.create_deck()
