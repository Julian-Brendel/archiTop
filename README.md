# archiTop
Archidekt to TableTop export cli
---
This project aims to smoothen the export process from a constructed [Magic the Gathering](https://magic.wizards.com/en) card deck in [Archidekt](https://archidekt.com/) to the game [TableTop Simulator](https://store.steampowered.com/app/286160/Tabletop_Simulator/).

## Motivation
Currently, third third party tools do exist to aid with this process, but these are neither smooth to use 
nor do they fulfill all the features that would smoothen the magic experience.

The two most noteworthy alternatives are:

1. **[Frogtown](https://www.frogtown.me/)** 
    - Doesn't allow to import directly from tabletop, requiring user to export and import
    - Doesn't keep track of the card versions used in the deck (basic lands will update to the most recent) 
    - Usage is slow, two step process required to generate and download deck
    - Doesn't separate commander cards from main deck
    
2. **[Tabletop scryfall importer](https://steamcommunity.com/sharedfiles/filedetails/?id=1838051922)**
    - Unexpected behaviour when multiple people import at the same time
    - Doesn't include tokens in the exported deck
    - Doesn't separate commander cards from main deck 

## What does this tool do?
This tool converts an Archidekt deck into Tabletop Simulator json format, able to be imported onto any tabletop board.
The cards contained, deck-name and thumbnail will be extracted for given Archidekt deck-id. 

## Installation
This project requires python 3.8 or greater, mainly because the walrus operator was used across the codebase. 
[Pipenv](https://pypi.org/project/pipenv/) is used to manage dependencies.

Install all dependencies using
`pipenv install`

## Usage
The tool is used via the commandline, runnable with
`python archiTop <deckID>`

Additional usage information can be acquired via the command
`python archiTop -h`

## Roadmap
The current plans for the repository are being tracked via [github issues](https://github.com/Julian-Brendel/archiTop/issues).
