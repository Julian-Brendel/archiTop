"""Sourcefile containing functions to load and populate json templates"""
from collections import OrderedDict
from helper import explode_card_list
from copy import deepcopy
from typing import List

from data_types import Card
from resources.templates import (contained_objects_template,
                                 custom_deck_template,
                                 final_deck_template)


def create_contained_objects(card: Card) -> dict:
    template = deepcopy(contained_objects_template)

    template['CardID'] = card.id
    template['Nickname'] = card.name

    return template


def create_custom_deck(face_url) -> dict:
    template = deepcopy(custom_deck_template)

    template['FaceURL'] = face_url

    return template


def construct_deck(cards: List[Card]) -> dict:
    deck_template = deepcopy(final_deck_template)

    # create list with exploded cards (one card per quantity)
    exploded_cards = explode_card_list(cards)

    object_states = deck_template['ObjectStates']

    contained_objects = [create_contained_objects(card)
                         for card in exploded_cards]

    custom_deck = OrderedDict({str(key + 1): create_custom_deck(card.image_url)
                               for key, card in enumerate(cards)})

    main_board = object_states[0]

    main_board['ContainedObjects'] = contained_objects
    main_board['DeckIDs'] = [card.id for card in exploded_cards]
    main_board['CustomDeck'] = custom_deck

    deck_template['ObjectStates'] = [main_board]

    return deck_template
