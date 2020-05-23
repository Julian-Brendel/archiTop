"""Templates for TableTop deck creation"""

final_deck_template = {
  "ObjectStates": [
    {
      "Name": "DeckCustom",
      "ContainedObjects": [],
      "DeckIDs": [],
      "CustomDeck": {},
      "Transform": {
        "posX": 0,
        "posY": 1,
        "posZ": 0,
        "rotX": 0,
        "rotY": 180,
        "rotZ": 180,
        "scaleX": 1,
        "scaleY": 1,
        "scaleZ": 1
      }
    }
  ]
}

custom_deck_template = {
  "FaceURL": None,
  "BackURL": "https://www.frogtown.me/images/gatherer/CardBack.jpg",
  "NumHeight": 1,
  "NumWidth": 1,
  "BackIsHidden": True
}

contained_objects_template = {
  "CardID": None,
  "Name": "Card",
  "Nickname": None,
  "Transform": {
    "posX": 0,
    "posY": 0,
    "posZ": 0,
    "rotX": 0,
    "rotY": 180,
    "rotZ": 180,
    "scaleX": 1,
    "scaleY": 1,
    "scaleZ": 1
  }
}
