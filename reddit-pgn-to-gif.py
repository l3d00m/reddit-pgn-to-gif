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
        pgns = re.findall("\[pgn\\\\?\](.*?)\\\\?\[/pgn\\\\?\]", post[1], re.DOTALL | re.IGNORECASE)
        if len(pgns) > 0:
            print("pgn(s) detected")
            pgns = pgns[:11]

            gif_urls = []
            for pgn in pgns:
                print(pgn)
                gif_urls.append(pgn2gif.convert_pgn_to_gif(pgn))
            if len(gif_urls) > 0:
                reddit.post_to_reddit(gif_urls, post[0])
    time.sleep(20)
