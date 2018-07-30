import config
import requests

LICHESS_URL = "https://lichess.org/import"


def pgn_to_lichess(pgn):
    try:
        r = requests.post(LICHESS_URL, data={'pgn': pgn}, allow_redirects=False)
        result = r.headers.get("location")
        if result is not None and result != LICHESS_URL:
            return "http://lichess.org" + result
    except Exception as e:
        if config.DEBUG:
            raise
        print("Error converting pgn to lichess: " + format(e))
    return False
