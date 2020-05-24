"""Sourcefile containing class fetching deck information"""
from abc import ABC, abstractmethod
from functools import reduce
from typing import List

import requests

from data_types import Card, Deck


class DeckFetcher(ABC):
    base_url = None
    cards = []

    def __init__(self, deck_id: int):
        self.deck_id = deck_id

    def __repr__(self) -> str:
        total_count = reduce(lambda a, b: a + b.quantity, self.cards, 0)
        return f'DeckFetcher({total_count} total cards, {len(self.cards)} unique cards)'

    def _get_raw_deck_data(self) -> dict:
        return requests.get(self.base_url % self.deck_id).json()

    def get_deck(self) -> Deck:
        raw_deck_data = self._get_raw_deck_data()

        deck_name = self._parse_deck_name(raw_deck_data)
        thumbnail_url = self._parse_deck_thumbnail_url(raw_deck_data)

        thumbnail = requests.get(thumbnail_url).content

        filtered_card_data = list(filter(self._validate_single_card,
                                         self._parse_card_data(raw_deck_data)))

        self.cards = [self._parse_single_card(card) for card in filtered_card_data]

        # sort cards based on commander property
        self.cards = list(sorted(self.cards, key=lambda card: card.commander, reverse=True))

        return Deck(self.cards, deck_name, thumbnail)

    @abstractmethod
    def _parse_single_card(self, card: dict) -> Card:
        raise NotImplemented

    @staticmethod
    @abstractmethod
    def _parse_card_data(raw_deck_data) -> List[dict]:
        raise NotImplemented

    @staticmethod
    @abstractmethod
    def _parse_deck_name(raw_deck_data) -> str:
        raise NotImplemented

    @staticmethod
    @abstractmethod
    def _parse_deck_thumbnail_url(raw_deck_data) -> str:
        raise NotImplemented

    @staticmethod
    @abstractmethod
    def _validate_single_card(card: dict) -> bool:
        raise NotImplemented
