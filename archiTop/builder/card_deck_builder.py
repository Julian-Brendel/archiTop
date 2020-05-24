"""Sourcefile containing deck builder class for TableTop"""
from collections import OrderedDict
from copy import deepcopy
from typing import List

from data_types import Card
from resources import (card_asset_template, card_deck_template,
                       card_template)


class CardDeckBuilder:
    """Class to construct card_deck, contained in final TableTop asset"""
    card_deck_json = deepcopy(card_deck_template)

    current_card_id = 100
    current_card_asset_id = 1

    card_back_url = 'https://www.frogtown.me/images/gatherer/CardBack.jpg'
    contained_objects = []
    deck_ids = []
    custom_deck = OrderedDict()

    def __init__(self, cards: List[Card]):
        self.cards = cards

    def __repr__(self):
        unique_cards = len(set(self.deck_ids))
        return f'CardDeck({len(self.deck_ids)} total cards, {unique_cards} unique cards)'

    def _populate_card_template(self, card: Card):
        card_json = deepcopy(card_template)

        card_json['CardID'] = self.current_card_id
        card_json['Nickname'] = card.name

        # create one object per quantity
        for _ in range(card.quantity):
            self.contained_objects.append(card_json)
            self.deck_ids.append(self.current_card_id)

        self.current_card_id += 100

    def _populate_card_asset_template(self, card: Card):
        card_asset_json = deepcopy(card_asset_template)

        card_asset_json['FaceURL'] = card.image_url
        card_asset_json['BackURL'] = self.card_back_url

        self.custom_deck[str(self.current_card_asset_id)] = card_asset_json

        self.current_card_asset_id += 1

    def create_deck(self) -> dict:
        for card in self.cards:
            self._populate_card_template(card)
            self._populate_card_asset_template(card)

        self.card_deck_json['ContainedObjects'] = self.contained_objects
        self.card_deck_json['DeckIDs'] = self.deck_ids
        self.card_deck_json['CustomDeck'] = self.custom_deck

        return self.card_deck_json
