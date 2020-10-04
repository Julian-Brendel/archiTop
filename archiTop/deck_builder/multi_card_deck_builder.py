"""Sourcefile containing deck builder class for decks with multiple cards"""
from collections import OrderedDict
from copy import deepcopy

from archiTop.base_classes import DeckBuilder
from archiTop.resources import (card_asset_template, card_deck_template,
                                card_template)
from archiTop.scryfall.data_types import ScryfallCard


class MultiCardDeckBuilder(DeckBuilder):
    """"MultiCardDeckBuilder class implementing abstract DeckBuilder class.
    Used for card decks with multiple cards."""

    def __init__(self, *args):
        self.card_deck_json = deepcopy(card_deck_template)
        self.contained_objects = []
        self.deck_ids = []
        self.custom_deck = OrderedDict()
        super().__init__(*args)

    def __repr__(self):
        unique_cards = len(set(self.deck_ids))
        return f'CardDeck({len(self.deck_ids)} total cards, {unique_cards} unique cards)'

    def _populate_card_template(self, card: ScryfallCard):
        """Creates a new TableTop card object and fills information from card class.
        Each card in deck needs one card object, therefore cards with quantity > 1 will be
        duplicated.
        Same cards, even when duplicated will keep the same ID.

        Once populated, card object is inserted into contained_objects and id added to deck_ids.

        Args:
            card:   Card to create card object for
        """
        card_json = deepcopy(card_template)

        card_json['CardID'] = self.current_card_id
        card_json['Nickname'] = card.tabletop_name

        # create one object per quantity
        for _ in range(card.quantity):
            self.contained_objects.append(card_json)
            self.deck_ids.append(self.current_card_id)

        self.current_card_id += 100

    def _populate_card_asset_template(self, card: ScryfallCard):
        """Creates a new TableTop card asset object and fills with information from card class.
        There should only exist on card asset template for each unique card.
        Therefor cards with quantity > 1 do only get one card asset.

        Asset matching is done with insertion order of asset objects.
        Order in the ContainedObjects, DeckID's must match the order of card assets.

        Once populated, card asset is inserted in custom deck and asset id is incremented.

        Args:
            card:   Card to create asset for
        """
        card_asset_json = deepcopy(card_asset_template)

        card_asset_json['FaceURL'] = card.image_url
        card_asset_json['BackURL'] = self.card_back_url

        self.custom_deck[str(self.current_card_asset_id)] = card_asset_json

        self.current_card_asset_id += 1

    def create_deck(self) -> dict:
        """Create the json structure for the card deck containing multiple cards.

        Returns:
            TableTop card deck json containing multiple cards
        """
        for card in self.cards:
            self._populate_card_template(card)
            self._populate_card_asset_template(card)

        self.card_deck_json['ContainedObjects'] = self.contained_objects
        self.card_deck_json['DeckIDs'] = self.deck_ids
        self.card_deck_json['CustomDeck'] = self.custom_deck
        self.card_deck_json['Transform']['rotZ'] = 180 if self.hidden else 0

        return self.card_deck_json
