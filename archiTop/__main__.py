import argparse
from typing import List

from builder.final_deck_builder import FinalDeckBuilder
from config import default_deck_name
from data_types import Card
from deck_fetcher import ArchidektFetcher

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

builder = FinalDeckBuilder(deck_name, cards)
builder.construct_final_deck()
builder.save_deck()
