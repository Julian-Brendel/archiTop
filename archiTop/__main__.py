"""Entry-point for application"""
import argparse

from archiTop.scryfall import ScryfallDeckBuilder
from archiTop.deck_builder import DeckBuilderWrapper
from archiTop.deck_fetcher import ArchidektFetcher
from archiTop.config import get_spin_logger

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
    return parser.parse_args()


def main():
    args = setup_argparse()

    # fetch raw deck information (card names and count)
    deck = ArchidektFetcher(args.deckID).get_deck()

    # overwrite deckname if optional argument is specified
    deck.name = args.name if args.name else deck.name

    # enrich deck information with scryfall data (cmc, type_lines etc.)
    scryfall_deck = ScryfallDeckBuilder(deck).construct_deck()

    builder = DeckBuilderWrapper(scryfall_deck, custom_back_url=args.custom_back_url)
    builder.construct_final_deck()
    builder.save_deck(args.path)


if __name__ == '__main__':
    main()

