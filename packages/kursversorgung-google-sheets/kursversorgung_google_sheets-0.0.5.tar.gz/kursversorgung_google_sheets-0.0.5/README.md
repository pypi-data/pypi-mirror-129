# Kursversorgung in Google Sheets
This project contains the basic files to ```updateLast(), updateSecurityName(), updateLastSplits()``` in the following Google Sheets: 
- [Kursversorgung Warrants](https://docs.google.com/spreadsheets/d/118-bK-9Iu0DRJiML1OE3yoXIh6LtHVrArLrPeYhRmek)
- [Private Placements](https://docs.google.com/spreadsheets/d/1ZKO1kNXYg6xkr-vsfS4KmITfAt9J7jC6o0cBFlDuKXo)

In order to access the Sheets a Google Workspace Account is requires and permission needs to be granted.

For further information contact [Valentin Baier](mailto:baier@orcacapital.de?subject=Google%20Workspace%20Account).

## Installation
The package needs to be build with ```auto-py-to-exe``` with the generic parameters ``--onedir --windowed`` and the specific paramters including the following files:

#### Parameter --icon 
- software_update.ico
#### Parameter --add-data
- software_update.ico
- README.md
#### Parameter --hidden-import
- tzdata
- xbbg
- accessOutlookEmail
- blpapi
- pandas

## Setting up a SSH-Tunnel
The program requires an active SSH connection to the ``docker1.orca.local`` with ``port=22426`` and needs to listen to the ``localhost:8194`` in ``local`` mode. The authentication method is username and password.

## Usage
The ``Kursversorung.exe`` can be executed from any computer having the required SSH-Tunnel running.

To start the program, click "Start updating"

## License
This project is licensed by a MIT License.

## Project status
The current released version is 0.0.5.
