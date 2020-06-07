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

### Example
Let's take one of my decks as example.
Exporting the deck https://archidekt.com/decks/94674#Maximum_Borkdrive is as simple as copying the deck-id
In this case `94674`

By running the tool with the given deck-id:
`python archiDekt 94674`, archiTop will export the deck as TableTop Simulator compatible file, alongside the thumbnail used for the deck in Archidekt.

Both files created will be named accordingly to the deck name in Archidekt:
![Output Example](https://archi-top.s3.eu-west-2.amazonaws.com/architop-output-example.png)

Now all that's left to do is to move the two files into the TableTop Objects folder.
The directory can vary for your Tabletop installation, based on OS.

You can find the path via the Tabletop Simulator game configurations:
![Tabletop Objects](https://archi-top.s3.eu-west-2.amazonaws.com/tabletop-save-location.png)

All that's left to do now is move the two files to the mod save location, in my case
`~/Library/Tabletop\ Simulator/Saves/Saved\ Objects/`

Have fun playing 🎉
 
## Roadmap
The current plans for the repository are being tracked via [github issues](https://github.com/Julian-Brendel/archiTop/issues).
