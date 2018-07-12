# Reddit: PGN to gif converter

*Converts PGN in `[pgn][/pgn]` tags from /r/chess into multiple gifs hosted on imgur and leaves them as a reddit comment*

* Supports multiple PGN tags in a single post or comment
* Uses `python-chess` which has a lax and less error prone PGN parsing
* Outputs multiple speed variants
* Shows only the main line of a PGN

## Build instructions

1. Copy `config.default.py` to `config.py` and add your keys (for reddit and imgur)
2. Install dependencies with `pip3 install -r requirements.txt`
3. Run the script with `,/reddit-pgn-to-gif.py`
