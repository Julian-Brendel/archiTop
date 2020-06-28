"""Entry-point for application"""
import argparse

from deck_builder import DeckBuilderWrapper
from deck_fetcher import ArchidektFetcher
from scryfall import ScryfallDeckBuilder

# parse input
parser = argparse.ArgumentParser(description='Convert archidekt deck to TableTop')
parser.add_argument('deckID',
                    help='Archidekt deck-ID to convert')
parser.add_argument('-n', '--name', type=str,
                    help='Optional deckname to overwrite the archidekt deckname')
parser.add_argument('-c', '-custom', action='store_true',
                    help='Use custom card-back, configured in config.ini')
args = parser.parse_args()

# fetch raw deck information (card names and count)
deck = ArchidektFetcher(args.deckID).get_deck()

# overwrite deckname if optional argument is specified
deck.name = args.name if args.name else deck.name

# enrich deck information with scryfall data (cmc, type_lines etc.)
scryfall_deck = ScryfallDeckBuilder(deck).construct_deck()

builder = DeckBuilderWrapper(scryfall_deck, custom_back=args.c)
builder.construct_final_deck()
builder.save_deck()
