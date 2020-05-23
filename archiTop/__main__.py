from archidekt import get_archidekt_deck
from deck_construction import construct_deck
import json

deck_id = 72608


# fetch deck data, (name and images of cards)
cards = get_archidekt_deck(deck_id)

deck = construct_deck(cards)

# save deck
json.dump(deck, open('deck.json', 'w'))
