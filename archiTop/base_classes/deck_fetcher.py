"""Sourcefile containing class fetching deck information"""
from abc import ABC, abstractmethod
from functools import reduce
from typing import List

import requests

from archiTop.config import getLogger
from archiTop.data_types import RawCard, RawDeck

logger = getLogger(__name__)


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

    def _get_raw_deck_data(self) -> dict:
        """Fetch the deck information by querying base_url combined with the deckID.

        Returns:
            Deck information in json format
        """
        logger.debug('Downloading deck <%s>', self.deck_id)
        return requests.get(self.base_url % self.deck_id).json()

    def get_deck(self) -> RawDeck:
        """Fetches and parses deck information.

        Returns:
            Deck of cards, containing deck information fetched
        """
        raw_deck_data = self._get_raw_deck_data()

        deck_name = self._parse_deck_name(raw_deck_data)
        thumbnail_url = self._parse_deck_thumbnail_url(raw_deck_data)

        thumbnail = requests.get(thumbnail_url).content

        filtered_mainboard_card_data = list(filter(self._validate_single_card_mainboard,
                                                   self._parse_card_data(raw_deck_data)))

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
    def _validate_single_card_mainboard(card: dict) -> bool:
        """Abstractmethod to be implemented by child class.
        Validates whether a single card belongs to mainboard.

        Args:
            card:   Card json object contained in fetched deck information

        Returns:
            True when card is contained in mainboard, False otherwise
        """
        raise NotImplemented
