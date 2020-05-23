"""Sourcefile containing functions to load and populate json templates"""
import json
from typing import List
from collections import OrderedDict


def create_contained_objects(card_id: int,
                             card_nickname: str) -> dict:
    template = json.load(open('resources/templates/contained_objects_template.json', 'r'))

    template['CardID'] = card_id
    template['Nickname'] = card_nickname

    return template


def create_custom_deck(face_url) -> dict:
    template = json.load(open('resources/templates/custom_deck_template.json', 'r'))

    template['FaceURL'] = face_url

    return template


def construct_deck(cards: List[str]) -> dict:
    # random card image url
    image_url = 'https://img.scryfall.com/cards/large/front/2/c/2c209efe-b4dc-44a3-bd45-d647f5680cbe.jpg?1568003729'

    deck_template = json.load(open('resources/templates/deck_template.json', 'r'))
    object_states = deck_template['ObjectStates']

    # produce main board
    card_ids = [x * 100 for x in range(1, len(cards) + 1)]

    contained_objects = [create_contained_objects(card_id, card_name)
                         for card_name, card_id in zip(cards, card_ids)]

    custom_deck = OrderedDict({str(key): create_custom_deck(image_url)
                               for key in range(1, len(cards) + 1)})

    main_board = object_states[0]

    main_board['ContainedObjects'] = contained_objects
    main_board['DeckIDs'] = card_ids
    main_board['CustomDeck'] = custom_deck

    deck_template['ObjectStates'] = [main_board]

    return deck_template


deck = construct_deck(['Grenzo Havoc Raiser', 'Mountain'])

json.dump(deck, open('../documents/test.json', 'w'))
