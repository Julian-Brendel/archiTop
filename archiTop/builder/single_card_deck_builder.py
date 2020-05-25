"""Sourcefile containing deck builder class for decks with one card"""
from copy import deepcopy

from base_classes import DeckBuilder
from resources import card_asset_template, card_template


class SingleCardDeckBuilder(DeckBuilder):
    """SingleCardDeckBuilder class implementing abstract DeckBuilder class.
    Used for card decks with single card."""
    card_json = deepcopy(card_template)

    def __repr__(self):
        return f'CardDeck({self.cards[0]})'

    def create_deck(self) -> dict:
        """Create the json structure for the card deck containing a single card.

        Returns:
            TableTop card deck json containing only a single card
        """
        card = self.cards[0]

        self.card_json['CardID'] = self.current_card_id
        self.card_json['Nickname'] = card.name

        card_asset_json = deepcopy(card_asset_template)
        card_asset_json['FaceURL'] = card.image_url
        card_asset_json['BackURL'] = self.card_back_url
        card_asset_json['BackIsHidden'] = False

        self.card_json['CustomDeck'] = {"1": card_asset_json}
        self.card_json['Transform']['rotZ'] = 180 if self.hidden else 0

        return self.card_json
