"""Sourcefile containing class to interact with archidekt services"""
from typing import List

from archiTop.base_classes import DeckFetcher
from archiTop.data_types import RawCard


class ArchidektFetcher(DeckFetcher):
    """ArchidektFetcher class, implementing abstract baseclass DeckFetcher"""
    base_url = 'https://archidekt.com/api/decks/%s/small/'

    def _parse_single_card(self, card: dict) -> RawCard:
        """Parses single card information from deck service into Card object.

        Args:
            card:   Card json object to parse information from

        Returns:
            Card class containing parsed information from card json object
        """
        card_data = card['card']

        name = card_data['oracleCard']['name']
        quantity = card['quantity']

        edition_code = card_data['edition']['editioncode']
        commander = card['category'] == 'Commander' or 'Commander' in card.get('categories', ())

        return RawCard(name, quantity, edition_code, commander)

    @staticmethod
    def _parse_card_data(raw_deck_data: dict) -> List[dict]:
        """Parses card information from deck data fetched by `_get_raw_deck_data()`.

        Args:
            raw_deck_data:  Raw server data fetched by deck data request

        Returns:
            List of card json objects contained in deck
        """
        return raw_deck_data['cards']

    @staticmethod
    def _parse_deck_name(raw_deck_data: dict) -> str:
        """Parses deck name from deck data fetched by `_get_raw_deck_data()`.

        Args:
            raw_deck_data:  Raw server data fetched by deck data request

        Returns:
            Name of deck
        """
        return raw_deck_data['name']

    @staticmethod
    def _parse_deck_thumbnail_url(raw_deck_data: dict) -> str:
        """Parses thumbnail url from deck data fetched by `_get_raw_deck_data()`.
        Args:
            raw_deck_data:  Raw server data fetched by deck data request

        Returns:
            Thumbnail url for fetched deck information
        """
        return raw_deck_data['featured']

    @staticmethod
    def _validate_single_card_mainboard(card: dict) -> bool:
        """Validates whether a single card belongs to mainboard.

        Args:
            card:   Card json object contained in fetched deck information

        Returns:
            True when card is contained in mainboard, False otherwise
        """
        blacklist = ('Maybeboard', 'Sideboard')
        category_check = card['category'] not in blacklist
        categories_checks = not any([blacklist_entry in card.get('categories', ())
                                     for blacklist_entry in blacklist])

        return category_check and categories_checks
