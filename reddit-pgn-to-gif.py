#!/usr/bin/env python3

import re
import time

import config
from pgn2gif import convert_pgn_to_gif
import reddit
from pgn2lichess import pgn_to_lichess

if config.DEBUG:
    config.subreddit = config.debug_subreddit


class Game:
    def __init__(self, album_url, lichess_url):
        self.album_url = album_url
        self.lichess_url = False if (lichess_url is None or lichess_url == "") else lichess_url


while 1:
    posts = reddit.get_new_posts()
    for post in posts:
        print(post.text)
        pgns = re.findall("\\[pgn\\](.*?)\\[/pgn\\]", post.text, re.DOTALL | re.IGNORECASE)
        if len(pgns) > 0:
            print("pgn(s) detected")
            # Maximum 10 PGNs
            pgns = pgns[:11]

            games = []
            for pgn in pgns:
                print(pgn)
                album_url = False
                try:
                    album_url = convert_pgn_to_gif(pgn)
                except Exception as e:
                    if config.DEBUG:
                        raise
                    print("Unknown error converting gif: " + format(e))
                if album_url is None or album_url is False:
                    continue
                lichess_url = pgn_to_lichess(pgn)
                print(lichess_url)
                games.append(Game(lichess_url=lichess_url, album_url=album_url))
            if len(games) > 0:
                reddit.post_to_reddit(games, post.reddit_object)
    time.sleep(30)
