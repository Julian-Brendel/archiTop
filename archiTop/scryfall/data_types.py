from dataclasses import dataclass
from functools import reduce
from typing import List

from archiTop.scryfall.scryfall_loader import load_scryfall_id_index


class ScryfallCard:
    """Class containing information for scryfall card object."""
    related_cards = set()

    def __init__(self,
                 scryfall_card_data: dict,
                 resolve_tokens=True,
                 quantity=1,
                 commander=False,
                 card_side=0,
                 altered_url: str = None):
        self.id_index = load_scryfall_id_index()

        self.commander = commander
        self.quantity = quantity
        self.name = scryfall_card_data['name']
        self.type_line = scryfall_card_data['type_line']
        self.cmc = scryfall_card_data['cmc']

        cmc_string = f'CMC{int(self.cmc)}'
        self.tabletop_name = f'{self.name} - {cmc_string}\n' \
                             f'{self.type_line}'

        self.id = scryfall_card_data['id']

        if altered_url:
            self.image_url = altered_url

        else:
            if 'image_uris' in scryfall_card_data:
                # extract image_url, choosing high rez if available
                image_uris = scryfall_card_data['image_uris']

            elif 'card_faces' in scryfall_card_data:  # card is a double sized card
                image_uris = scryfall_card_data['card_faces'][card_side]['image_uris']

                if card_side == 0:
                    self.related_cards = {ScryfallCard(self.id_index[scryfall_card_data['id']],
                                                       resolve_tokens=False,
                                                       card_side=1)}

            else:
                raise Exception('Unknown card-type encountered')

            if 'large' in image_uris:
                self.image_url = image_uris['large']
            else:
                self.image_url = image_uris['normal']

        if resolve_tokens:
            related_objects = scryfall_card_data.get('all_parts', ())

            related_tokens = list(
                    filter(lambda related_object: related_object['component'] == 'token',
                           related_objects))
            related_meld_cards = list(
                    filter(lambda related_object: related_object['component'] == 'meld_result',
                           related_objects))

            related_ids = set([related_object['id'] for related_object in
                               related_tokens + related_meld_cards])

            self.related_cards |= {ScryfallCard(self.id_index[related_id],
                                                resolve_tokens=False)
                                   for related_id in related_ids}

    def __repr__(self):
        commander_identifier = '[Commander]' if self.commander else ''
        return f'Card{commander_identifier}({self.quantity: <2} x {self.name})'

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, ScryfallCard):
            return self.id == other.id

        return False

    def __hash__(self):
        return hash(self.id)


@dataclass
class ScryfallDeck:
    """Class containing information for mtg deck of cards.
        This consists of the mainboard, sideboard and token / emblems."""
    mainboard: List[ScryfallCard]  # list containing cards in mainboard
    related_cards: List[ScryfallCard]  # list containing related cards (tokens, ...)
    name: str  # name of deck
    thumbnail: bytes  # image bytes for deck thumbnail

    def __repr__(self):
        total_count = reduce(lambda a, b: a + b.quantity, self.mainboard, 0)
        return (f'Deck[{self.name}](\n'
                f'- {total_count: <3} total cards\n'
                f'- {len(self.mainboard): <3} unique cards\n'
                f'- {len(self.related_cards): <3} related cards)')
