"""Sourcefile containing class to interact with archidekt services"""
from typing import List

from base_classes import DeckFetcher
from data_types import Card


class ArchidektFetcher(DeckFetcher):
    base_url = 'https://archidekt.com/api/decks/%s/small/'
    image_url = 'https://storage.googleapis.com/archidekt-card-images/%s/%s_normal.jpg'

    def _parse_single_card(self, card: dict) -> Card:
        card_data = card['card']

        edition_code = card_data['edition']['editioncode']
        uid = card_data['uid']

        name = card_data['oracleCard']['name']
        image_url = self.image_url % (edition_code, uid)
        quantity = card['quantity']

        return Card(name, image_url, quantity)

    @staticmethod
    def _parse_card_data(raw_deck_data) -> List[dict]:
        return raw_deck_data['cards']

    @staticmethod
    def _validate_single_card(card: dict) -> bool:
        return card['category'] not in ('Maybeboard', 'Sideboard')

    @staticmethod
    def _parse_deck_name(raw_deck_data) -> str:
        return raw_deck_data['name']

    @staticmethod
    def _parse_deck_thumbnail_url(raw_deck_data) -> str:
        return raw_deck_data['featured']
