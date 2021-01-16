"""Entry-point for application"""
import argparse
import json

from archiTop.config import get_spin_logger
from archiTop.deck_builder import DeckBuilderWrapper
from archiTop.deck_fetcher import ArchidektFetcher
from archiTop.scryfall import ScryfallDeckBuilder

spin_logger = get_spin_logger(__name__)


def setup_argparse():
    parser = argparse.ArgumentParser(description='Convert archidekt deck to TableTop')
    parser.add_argument('deckID',
                        help='Archidekt deck-ID to convert')
    parser.add_argument('-n', '--name', type=str,
                        help='Optional deckname to overwrite the archidekt deckname')
    parser.add_argument('-c', '--custom_back_url', type=str,
                        help='Use custom card-back image url')
    parser.add_argument('-p', '--path', type=str,
                        help='Path to write output to')
    parser.add_argument('-a', '--altered', type=str,
                        help='File containing image-urls by card name to use instead of scryfall')
    return parser.parse_args()


def main():
    args = setup_argparse()

    # fetch raw deck information (card names and count)
    deck = ArchidektFetcher(args.deckID).get_deck()

    # overwrite deckname if optional argument is specified
    deck.name = args.name if args.name else deck.name

    altered_cards_index = json.load(open(args.altered, "r")) if args.altered else {}

    # enrich deck information with scryfall data (cmc, type_lines etc.)
    scryfall_deck = ScryfallDeckBuilder(deck, altered_cards_index).construct_deck()

    builder = DeckBuilderWrapper(scryfall_deck, custom_back_url=args.custom_back_url)
    builder.construct_final_deck()
    builder.save_deck(args.path)


if __name__ == '__main__':
    main()
