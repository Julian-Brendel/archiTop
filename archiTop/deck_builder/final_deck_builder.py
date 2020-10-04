"""Sourcefile containing final deck builder class for TableTop"""
import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import List, Optional

from archiTop.config import getLogger, load_config
from archiTop.deck_builder.multi_card_deck_builder import MultiCardDeckBuilder
from archiTop.deck_builder.single_card_deck_builder import SingleCardDeckBuilder
from archiTop.resources import final_deck_template
from archiTop.scryfall.data_types import ScryfallCard, ScryfallDeck

logger = getLogger(__name__)


class DeckBuilderWrapper:
    """Wrapper class, converting Deck object into TableTop deck asset"""
    custom_back_url = None

    def __init__(self,
                 deck: ScryfallDeck,
                 custom_back_url: str = None):
        """Initializes deck builder wrapper with deck of cards.

        Args:
            deck:               Deck including cards contained and additional deck information
            custom_back_url:    Url for image to replace the default mtg card-back
        """
        self.final_deck_json = deepcopy(final_deck_template)
        self.card_decks = []

        self.deck = deck
        if custom_back_url:
            logger.debug('Using custom card-back <%s>', custom_back_url)
            self.custom_back_url = custom_back_url

    def construct_final_deck(self):
        """Constructs the final asset json for TableTop.
        Separates mainboard cards from commander, then creates multiple card decks
        for mainboard- and commander-cards.
        """
        mainboard_cards = list(filter(lambda card: not card.commander, self.deck.mainboard))
        commander_cards = list(filter(lambda card: card.commander, self.deck.mainboard))

        # construct related cards card-deck, including tokens
        if token_deck := self._construct_card_deck(self.deck.related_cards, hidden=False):
            self.card_decks.append(token_deck)

        # construct mainboard card-deck
        if mainboard_deck := self._construct_card_deck(mainboard_cards):
            self.card_decks.append(mainboard_deck)

        # construct separate card-deck for commander
        if commander_deck := self._construct_card_deck(commander_cards, hidden=False):
            self.card_decks.append(commander_deck)

        # todo: implement sideboard
        # construct sideboard
        if sideboard_deck := None:
            self.card_decks.append(sideboard_deck)

        # shift deck positions so piles do not combine
        current_x_pos = 0
        for deck in self.card_decks:
            deck['Transform']['posX'] = current_x_pos
            current_x_pos += 2.2

        self.final_deck_json['ObjectStates'] = self.card_decks

    def save_deck(self, export_location: str = None):
        """Saves deck and thumbnail.
        Filename is determined by the chosen deck name.

        If system is mac os, output will be saved to the tabletop location,
        otherwise it will be stored to current directory.

        Args:
            export_location:    Optional argument to overwrite output location
        """
        deck_name = f'{self.deck.name}.json'
        thumbnail_name = f'{self.deck.name}.png'

        if export_location:
            logger.debug(f'Saving deck <{self.deck.name}> to passed location {export_location}')

        else:
            if sys.platform == 'darwin':  # client is using mac os
                logger.debug(f'Saving deck <{self.deck.name}> to tabletop location')
                table_top_save_location = load_config()['EXPORT']['MAC']
                export_location = Path(Path.home(), table_top_save_location)

            else:
                logger.debug(f'Saving deck <{self.deck.name}> to current directory')
                export_location = ''

        # save deck json
        json.dump(self.final_deck_json, open(Path(export_location, deck_name), 'w'))
        # save deck thumbnail
        with open(Path(export_location, thumbnail_name), 'wb') as file:
            file.write(self.deck.thumbnail)

    def _construct_card_deck(self, card_list: List[ScryfallCard],
                             hidden=True) -> Optional[dict]:
        """Chooses DeckBuilder based on amount of amount of cards passed.

        Chooses SingleCardDeckBuilder when card list contains a single card.
        MultiCardDeckBuilder when card list contains multiple cards.

        Args:
            card_list:  List of cards to create deck asset for
            hidden:     Whether deck is hidden or not (face down)
                        Defaults to true.

        Returns:
            Result from deck builder or None when List is empty
        """
        if len(card_list) > 1:
            builder = MultiCardDeckBuilder(card_list, hidden, self.custom_back_url)
        elif len(card_list) == 1:
            builder = SingleCardDeckBuilder(card_list, hidden, self.custom_back_url)
        else:
            logger.warning('Passed card list is empty')
            return None

        return builder.create_deck()
