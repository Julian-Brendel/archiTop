"""Sourcefile containing helper functions for codebase"""
from typing import List

from data_types import Card


def explode_card_list(cards: List[Card]) -> List[Card]:
    exploded_cards = [x for y in [card.explode() for card in cards] for x in y]

    return exploded_cards
