#!/usr/bin/env python3

import re
import time

import config
import pgn2gif
import reddit

if config.DEBUG:
    config.subreddit = config.debug_subreddit

while 1:
    posts = reddit.get_new_posts()
    for post in posts:
        reddit_object = post[0]
        body = post[1]

        pgns = re.findall("\[pgn\\\\?\](.*?)\\\\?\[/pgn\\\\?\]", body, re.DOTALL | re.IGNORECASE)
        if len(pgns) > 0:
            print("pgn(s) detected")
            # Maximum 10 PGNs
            pgns = pgns[:11]

            games = []
            for pgn in pgns:
                print(pgn)
                try:
                    album_url = pgn2gif.convert_pgn_to_gif(pgn)
                except Exception as e:
                    if config.DEBUG:
                        raise
                    else:
                        print("Unknown error converting gif: " + format(e))
                        continue
                if album_url is None:
                    continue
                games.append(album_url)
            if len(games) > 0:
                reddit.post_to_reddit(games, reddit_object)
    time.sleep(30)
