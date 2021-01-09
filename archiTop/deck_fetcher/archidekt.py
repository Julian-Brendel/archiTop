"""Sourcefile containing class to interact with archidekt services"""
from typing import List, Set

import requests

from archiTop.base_classes import DeckFetcher, DeckFetcherError
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
        uid = card_data['uid']
        quantity = card['quantity']

        edition_code = card_data['edition']['editioncode']
        commander = card['category'] == 'Commander' or 'Commander' in card.get('categories', ())

        return RawCard(name, quantity, uid, edition_code, commander)

    @staticmethod
    def _handle_raw_deck_request(response: requests.Response):
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
    def _parse_mainboard_identifier(raw_deck_data: dict) -> Set[str]:
        """Extracts valid categories for cards belonging to mainboard.
        Archidekt has functionality of marking categories as not included in the deck,
        these are being filtered out.

        Args:
            raw_deck_data:      Raw json response data from archidekt api

        Returns:
            Set containing valid categories
        """
        valid_categories = {category['name'] for category in raw_deck_data['categories']
                            if category['includedInDeck']}
        return valid_categories - {'Sideboard'}

    @staticmethod
    def _validate_single_card_mainboard(card: dict, mainboard_identifier: Set[str]) -> bool:
        """Validates whether a single card belongs to mainboard.

        Args:
            card:                   Card json object contained in fetched deck information
            mainboard_identifier:   List holding valid mainboard categories

        Returns:
            True when card is contained in mainboard, False otherwise
        """
        # return category_check and categories_checks
        category = card['categories'][0] if len(card['categories']) > 0 else None

        return category in mainboard_identifier
