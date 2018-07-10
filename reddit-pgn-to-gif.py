#!/usr/bin/env python3

import praw
import re
import config
import io
import chess
import chess.pgn
import chess.svg
import cairosvg
import imageio
from giphypop import upload
import time

reddit = praw.Reddit(client_id=config.reddit_client_id,
                     client_secret=config.reddit_client_secret,
                     user_agent='python3 script for converting /r/chess PGNs to GIFs',
                     username=config.reddit_username,
                     password=config.reddit_password)

posted_to = []


def parse_pgns(content):
    pgns = re.findall("\[pgn\\\\?\](.*?)\\\\?\[/pgn\\\\?\]", content, re.DOTALL | re.IGNORECASE)
    if len(pgns) > 0:
        print("pgn(s) detected")
        gif_urls = []
        for pgn in pgns:
            print(pgn)
            gif_urls.append(convert_pgn_to_gif(pgn))
        return gif_urls


def convert_pgn_to_gif(pgn):
    pgn_file = io.StringIO(str(pgn))
    game = chess.pgn.read_game(pgn_file)
    board = game.board()
    images = [position_to_image(board)]
    for move in game.main_line():
        board.push(move)
        images.append(position_to_image(board))
    imageio.mimsave('fast.gif', images, duration=1)
    imageio.mimsave('slow.gif', images, duration=4)
    gif_slow = upload(["chess"], 'slow.gif')
    gif_fast = upload(["chess"], 'fast.gif')
    return [gif_slow.media_url, gif_fast.media_url]


def position_to_image(board):
    svg_string = chess.svg.board(board)
    # noinspection PyUnresolvedReferences
    cairosvg.svg2png(bytestring=svg_string, write_to="output.png")
    return imageio.imread("output.png")


def post_to_reddit(gif_urls, rsubmission):
    text = "I've converted your PGNs into GIFs:\n\n"
    for game_urls in gif_urls:
        text += "[Slow variant](" + game_urls[0] + ")  \n"
        text += "[Fast variant](" + game_urls[1] + ")\n\n"
    text += "----\n\n*I'm a Bot for /r/chess. " \
            "For a better experience, install the PGN Viewer addon " \
            "for [firefox](https://addons.mozilla.org/en-US/firefox/addon/reddit-pgn-viewer/) or " \
            "[chrome](https://chrome.google.com/webstore/detail/reddit-pgn-viewer/hplecpnihkigeaiobbmfnfblepiadjdh)*"
    print("replying with: " + text + " to " + submission.shortlink)
    rsubmission.reply(text)


def load_posted_to():
    redditor = reddit.redditor(config.reddit_username)
    for comment in redditor.comments.new(limit=100):
        posted_to.append(comment.parent_id)


load_posted_to()

while 1:
    for submission in reddit.subreddit(config.subreddit).new(limit=20):
        if submission.is_self and submission.selftext != "":
            if submission.name in posted_to:
                print("Already posted to")
                continue
            urls = parse_pgns(submission.selftext)
            if urls is not None and len(urls) > 0:
                post_to_reddit(urls, submission)
            posted_to.append(submission.name)

    for comment in reddit.subreddit(config.subreddit).comments(limit=30):
        if comment.name in posted_to:
            print("Already posted to")
            continue
        if comment.author.name.lower() == config.reddit_username.lower():
            continue
        urls = parse_pgns(comment.body)
        if urls is not None and len(urls) > 0:
            post_to_reddit(urls, comment)
        posted_to.append(comment.name)
    time.sleep(20)
