"""Templates for TableTop deck creation"""

# template for the final json to be imported into TableTop
final_deck_template = {
    "ObjectStates": []  # <-- card_deck_templates go here
}

# template for each deck of cards in the TableTop asset (I.e: MainBoard, SideBoard, Tokens)
card_deck_template = {
    "Name": "DeckCustom",
    "ContainedObjects": [],  # <-- card_templates go here
    "DeckIDs": [],  # <-- all cardID's from card_templates go here in order
    "CustomDeck": {},  # <-- card_asset_templates go here.
    # Notation is {"1": <card_asset_template>, "2": <>...}, same ordering as card_templates
    "Transform": {
        "posX": 0,
        "posY": 1,
        "posZ": 0,
        "rotX": 0,
        "rotY": 0,
        "rotZ": 180,
        "scaleX": 1,
        "scaleY": 1,
        "scaleZ": 1
    }
}

# template for each card in the deck
# cardID should be ascending
# cards with quantity > 1 require multiple entries with the same card id
card_template = {
    "Name": "Card",
    "CardID": None,
    "Nickname": None,
    "Transform": {
        "posX": 0,
        "posY": 0,
        "posZ": 0,
        "rotX": 0,
        "rotY": 0,
        "rotZ": 180,
        "scaleX": 1,
        "scaleY": 1,
        "scaleZ": 1
    }
}

# template for card assets (back and front image)
# one entry for each unique card
card_asset_template = {
    "FaceURL": None,
    "BackURL": None,
    "NumHeight": 1,
    "NumWidth": 1,
    "BackIsHidden": True
}
