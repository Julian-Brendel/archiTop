import argparse
import json
from typing import List

from data_types import Card
from deck_fetcher import ArchidektFetcher
from config import default_deck_name
from deck_construction import construct_deck

# parse input
parser = argparse.ArgumentParser(description='Convert archidekt deck to TableTop')
parser.add_argument('deckID',
                    help='Archidekt deck-ID to convert')
parser.add_argument("--name", type=str,
                    help="Deckname")
args = parser.parse_args()

deck_name = args.name if args.name else default_deck_name

fetcher = ArchidektFetcher(args.deckID)

# fetch deck data, (name, image and quantity of cards)
cards: List[Card] = fetcher.get_cards()

deck = construct_deck(cards)

# save deck
json.dump(deck, open(f'{deck_name}.json', 'w'))
