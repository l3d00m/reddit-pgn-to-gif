# Reddit: PGN to gif converter

*Converts PGN in `[pgn][/pgn]` tags from http://reddit.com/r/chess (among other subreddits) into gifs hosted on imgur and to a [lichess analysis board](https://lichess.org/analysis). It comments the links as a reply on reddit.*

* Supports multiple PGN tags in a single post or comment
* Uses [`python-chess`](https://github.com/niklasf/python-chess) which has a lax PGN parsing
* Conversion to GIF using [`lila-gif`](https://github.com/niklasf/lila-gif) (with the nice lichess chess board theme)
* Outputs multiple speed variants as an imgur album
* *Only the main line of a PGN is supported*

Examples can be seen on reddit: http://reddit.com/u/PGNtoGIF 

## Build instructions

1. Build [`lila-gif`](https://github.com/niklasf/lila-gif) and run it
2. Copy `config.default.py` to `config.py` and add your keys (for reddit and imgur)
3. Install dependencies with `pip3 install -r requirements.txt`
4. Run the script with `./reddit-pgn-to-gif.py`
