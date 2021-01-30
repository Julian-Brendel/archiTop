"""Sourcefile containing class to interact with moxfield services"""
from typing import List, Set

import requests

from archiTop.base_classes import DeckFetcher, DeckFetcherError
from archiTop.data_types import RawCard
from archiTop.scryfall import load_scryfall_id_index


class MoxfieldFetcher(DeckFetcher):
    """MoxfieldFetcher class, implementing abstract baseclass DeckFetcher"""
    base_url = ' https://api.moxfield.com/v2/decks/all/%s'
    scryfall_id_index = load_scryfall_id_index()

    @staticmethod
    def _parse_card(data: dict, commander: bool = False) -> RawCard:
        """Parses single card information from deck service into Card object.

        Args:
            card:   Card json object to parse information from

        Returns:
            Card class containing parsed information from card json object
        """
        quantity = data['quantity']
        name = data['card']['name']
        uid = data['card']['scryfall_id']

        return RawCard(name, quantity, uid, commander)

    @staticmethod
    def _handle_response(response: requests.Response):
        """Handles response from moxfield api, validating request was successful.

        Raises:
            DeckFetcherError: When invalid status code was encountered in response from api

        Args:
            response:   Response object from archidekt api call
        """
        try:
            response.raise_for_status()

        except requests.HTTPError as e:
            raise DeckFetcherError(f'Failed to fetch moxfield deck with error:\n{e}')

    def _parse_mainboard_cards(self, data: dict) -> List[RawCard]:
        """Parses card information from deck data fetched by `_get_raw_deck_data()`.

        Args:
            raw_deck_data:  Raw server data fetched by deck data request

        Returns:
            List of card json objects contained in deck
        """
        mainboard_cards = [self._parse_card(card) for card in data['mainboard'].values()]
        mainboard_cards += [self._parse_card(card, commander=True)
                            for card in data['commanders'].values()]
        return mainboard_cards

    @staticmethod
    def _parse_deck_name(data: dict) -> str:
        """Parses deck name from deck data fetched by `_get_raw_deck_data()`.

        Args:
            data:  Raw server data fetched by deck data request

        Returns:
            Name of deck
        """
        return data['name']

    def _get_thumbnail(self, data: dict) -> bytes:
        """Parses thumbnail url from deck data fetched by `_get_raw_deck_data()`.
        Args:
            data:  Raw server data fetched by deck data request

        Returns:
            Thumbnail url for fetched deck information
        """
        if data['commanders'].values():
            card = list(data['commanders'].values())[0]
            scryfall_card = self.scryfall_id_index[card['card']['scryfall_id']]

            image_uris = scryfall_card.get('image_uris') or scryfall_card.get('card_faces')[0][
                'image_uris']
            return requests.get(image_uris['art_crop']).content
