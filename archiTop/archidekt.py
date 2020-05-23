"""Sourcefile containing interaction with archidekt"""
from typing import List

import requests

from data_types import Card

api_url = 'https://archidekt.com/api/decks/%s/small/'
image_url = 'https://storage.googleapis.com/archidekt-card-images/%s/%s_normal.jpg'


def validate_card(card):
    return card['category'] != 'Maybeboard'


def extract_card_info(card, card_id) -> Card:
    card_data = card['card']

    edition_code = card_data['edition']['editioncode']
    uid = card_data['uid']

    return Card(
        card_id * 100,
        card_data['oracleCard']['name'],
        image_url % (edition_code, uid),
        card['quantity'])


def get_raw_deck_data(deck_id: int) -> dict:
    return requests.get(api_url % deck_id).json()


def parse_raw_deck_data(deck_data: dict) -> List[Card]:
    filtered_card_data = [card for card in deck_data['cards'] if validate_card(card)]
    cards = [extract_card_info(card, index + 1) for index, card in enumerate(filtered_card_data)]

    return cards


def get_archidekt_deck(deck_id: int) -> List[Card]:
    deck_data = get_raw_deck_data(deck_id)

    return parse_raw_deck_data(deck_data)
