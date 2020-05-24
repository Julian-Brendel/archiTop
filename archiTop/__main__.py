import argparse
from typing import List

from builder.final_deck_builder import DeckBuilderWrapper
from data_types import Card
from deck_fetcher import ArchidektFetcher

# parse input
parser = argparse.ArgumentParser(description='Convert archidekt deck to TableTop')
parser.add_argument('deckID',
                    help='Archidekt deck-ID to convert')
parser.add_argument("-n", '--name', type=str,
                    help="Optional deckname to overwrite the archidekt deckname")
args = parser.parse_args()

fetcher = ArchidektFetcher(args.deckID)

# fetch deck data, (name, image and quantity of cards)
deck = fetcher.get_deck()

# overwrite deckname if optional argument is specified
deck.name = args.name if args.name else deck.name

builder = DeckBuilderWrapper(deck)
builder.construct_final_deck()
builder.save_deck()
