"""Sourcefile containing class fetching deck information"""
from abc import ABC, abstractmethod
from functools import reduce
from typing import Any, List

import requests

from archiTop.config import get_spin_logger
from archiTop.data_types import RawCard, RawDeck

spin_logger = get_spin_logger(__name__)


class DeckFetcherError(Exception):
    """Exception to raise when an error was encountered during deck fetching"""
    pass


class DeckFetcher(ABC):
    """Abstract baseclass to for deck fetcher"""
    base_url = None
    mainboard_cards = []

    def __init__(self, deck_id: int):
        """Initializes deck fetcher with id of deck.

        Args:
            deck_id:    DeckID to fetch deck information for
        """
        self.deck_id = deck_id

    def __repr__(self) -> str:
        total_count = reduce(lambda a, b: a + b.quantity, self.mainboard_cards, 0)
        return f'DeckFetcher({total_count} total cards, {len(self.mainboard_cards)} unique cards)'

    def _request_raw_deck(self) -> requests.Response:
        """Fetch the deck information by querying base_url combined with the deckID.

        Returns:
            Deck information in json format
        """
        spin_logger.debug('Downloading deck <%s>', self.deck_id, extra={'user_waiting': True})
        response = requests.get(self.base_url % self.deck_id)
        spin_logger.debug('Downloaded deck <%s>', self.deck_id, extra={'user_waiting': False})
        return response

    @staticmethod
    def _parse_raw_deck_data(request: requests.Response) -> dict:
        return request.json()

    def get_deck(self) -> RawDeck:
        """Fetches and parses deck information.

        Returns:
            Deck of cards, containing deck information fetched
        """
        raw_deck_response = self._request_raw_deck()

        self._handle_raw_deck_request(raw_deck_response)

        raw_deck_data = self._parse_raw_deck_data(raw_deck_response)

        deck_name = self._parse_deck_name(raw_deck_data)
        thumbnail_url = self._parse_deck_thumbnail_url(raw_deck_data)

        thumbnail = requests.get(thumbnail_url).content

        mainboard_identifier = self._parse_mainboard_identifier(raw_deck_data)
        filtered_mainboard_card_data = [
                card for card in self._parse_card_data(raw_deck_data)
                if self._validate_single_card_mainboard(card, mainboard_identifier)]

        self.mainboard_cards = [self._parse_single_card(card) for card in
                                filtered_mainboard_card_data]

        return RawDeck(self.mainboard_cards, deck_name, thumbnail)

    @abstractmethod
    def _parse_single_card(self, card: dict) -> RawCard:
        """Abstractmethod to be implemented by child class.
        Parses single card information from deck service into Card object.

        Args:
            card:   Card json object to parse information from

        Returns:
            Card class containing parsed information from card json object
        """
        raise NotImplemented

    @staticmethod
    @abstractmethod
    def _handle_raw_deck_request(response: requests.Response):
        """Abstractmethod to be implemented by child class.
        Validates whether request to server was successful.

        Args:
            response:   Response from server request
        """
        raise NotImplemented

    @staticmethod
    @abstractmethod
    def _parse_card_data(raw_deck_data: dict) -> List[dict]:
        """Abstractmethod to be implemented by child class.
        Parses card information from deck data fetched by `_get_raw_deck_data()`.

        Args:
            raw_deck_data:  Raw server data fetched by deck data request

        Returns:
            List of card json objects contained in deck
        """
        raise NotImplemented

    @staticmethod
    @abstractmethod
    def _parse_deck_name(raw_deck_data: dict) -> str:
        """Abstractmethod to be implemented by child class.
        Parses deck name from deck data fetched by `_get_raw_deck_data()`.

        Args:
            raw_deck_data:  Raw server data fetched by deck data request

        Returns:
            Name of deck
        """
        raise NotImplemented

    @staticmethod
    @abstractmethod
    def _parse_deck_thumbnail_url(raw_deck_data: dict) -> str:
        """Abstractmethod to be implemented by child class.
        Parses thumbnail url from deck data fetched by `_get_raw_deck_data()`.

        Args:
            raw_deck_data:  Raw server data fetched by deck data request

        Returns:
            Thumbnail url for fetched deck information
        """
        raise NotImplemented

    @staticmethod
    @abstractmethod
    def _validate_single_card_mainboard(card: dict, mainboard_identifier: Any) -> bool:
        """Abstractmethod to be implemented by child class.
        Validates whether a single card belongs to mainboard using the passed mainboard_identifier.

        Args:
            card:                   Card json object contained in fetched deck information
            mainboard_identifier:   Identifier to validate card belongs to mainboard

        Returns:
            True when card is contained in mainboard, False otherwise
        """
        raise NotImplemented

    @staticmethod
    @abstractmethod
    def _parse_mainboard_identifier(raw_deck_data: dict) -> Any:
        """Abstractmethod to be implemented by child class.
        Parses the identifier for mainboard cards from raw data fetched.

        Args:
            raw_deck_data:      Raw data fetched from server

        Returns:
            Identifier object
        """
        raise NotImplemented
