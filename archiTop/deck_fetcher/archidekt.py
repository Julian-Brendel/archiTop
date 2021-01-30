"""Sourcefile containing class to interact with archidekt services"""
from typing import List, Set

import requests

from archiTop.base_classes import DeckFetcher, DeckFetcherError
from archiTop.data_types import RawCard


class ArchidektFetcher(DeckFetcher):
    """ArchidektFetcher class, implementing abstract baseclass DeckFetcher"""
    base_url = 'https://archidekt.com/api/decks/%s/small/'

    @staticmethod
    def _parse_single_card(card: dict) -> RawCard:
        """Parses single card information from deck service into Card object.

        Args:
            card:   Card json object to parse information from

        Returns:
            Card class containing parsed information from card json object
        """
        card_data = card['card']

        name = card_data['oracleCard']['name']
        uid = card_data['uid']
        quantity = card['quantity']

        commander = card['category'] == 'Commander' or 'Commander' in card.get('categories', ())

        return RawCard(name, quantity, uid, commander)

    @staticmethod
    def _handle_response(response: requests.Response):
        """Handles response from archidekt api, validating request was successful.

        Raises:
            DeckFetcherError: When invalid status code was encountered in response from api

        Args:
            response:   Response object from archidekt api call
        """
        try:
            response.raise_for_status()

        except requests.HTTPError as e:
            try:
                error_message = response.json()['error']

            except Exception:
                error_message = e

            raise DeckFetcherError(f'Failed to fetch archidekt deck with error:\n{error_message}')

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
    def _get_thumbnail(raw_deck_data: dict) -> bytes:
        """Parses thumbnail url from deck data fetched by `_get_raw_deck_data()`.
        Args:
            raw_deck_data:  Raw server data fetched by deck data request

        Returns:
            Thumbnail url for fetched deck information
        """
        url = raw_deck_data['featured']
        return requests.get(url).content

    def _parse_mainboard_cards(self, data: dict) -> List[RawCard]:
        # identify categories for all valid mainboard cards
        valid_categories = {category['name'] for category in data['categories']
                            if category['includedInDeck']} - {'Sideboard'}

        mainboard_cards = [card for card in data['cards']
         if self._validate_mainboard_cards(card, valid_categories)]

        return [self._parse_single_card(card) for card in mainboard_cards]


    @staticmethod
    def _validate_mainboard_cards(card: dict, mainboard_categories: Set[str]) -> bool:
        """Validates whether a single card belongs to mainboard.

        Args:
            card:                   Card json object contained in fetched deck information
            mainboard_identifier:   List holding valid mainboard categories

        Returns:
            True when card is contained in mainboard, False otherwise
        """
        # return category_check and categories_checks
        category = card['categories'][0] if len(card['categories']) > 0 else None

        return category in mainboard_categories
