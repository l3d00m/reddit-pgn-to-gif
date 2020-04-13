# Reddit: PGN to gif converter

*Converts PGN in `[pgn][/pgn]` tags from http://reddit.com/r/chess into gifs hosted on imgur and to a [lichess analysis board](https://lichess.org/analysis). It comments the links as a reply on reddit.*

* Supports multiple PGN tags in a single post or comment
* Uses [`python-chess`](https://github.com/niklasf/python-chess) which has a lax PGN parsing
* Outputs multiple speed variants as an imgur album
* *Only the main line of a PGN is supported*

Examples can be seen on reddit: http://reddit.com/u/PGNtoGIF 

## Build instructions

1. Copy `config.default.py` to `config.py` and add your keys (for reddit and imgur)
2. Install dependencies with `pip3 install -r requirements.txt`
3. Run the script with `./reddit-pgn-to-gif.py`
