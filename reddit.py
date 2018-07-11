import praw
import config

reddit = praw.Reddit(client_id=config.reddit_client_id,
                     client_secret=config.reddit_client_secret,
                     user_agent='python3 script for converting /r/chess PGNs to GIFs',
                     username=config.reddit_username,
                     password=config.reddit_password)

posted_to = []


def get_new_posts():
    to_return = []
    subr = reddit.subreddit(config.subreddit)

    if len(posted_to) == 0:
        redditor = reddit.redditor(config.reddit_username)
        for comment in redditor.comments.new(limit=100):
            posted_to.append(comment.parent_id)

    for submission in subr.new(limit=20):
        if submission.name in posted_to:
            if config.DEBUG:
                print("Already posted to")
            continue
        if submission.is_self and submission.selftext != "":
            to_return.append([submission, str(submission.selftext)])
        posted_to.append(submission.name)

    for comment in subr.comments(limit=30):
        if comment.author.name.lower() == config.reddit_username.lower():
            continue
        if comment.name in posted_to:
            if config.DEBUG:
                print("Already posted to")
            continue
        to_return.append([comment, str(comment.body)])
        posted_to.append(comment.name)
    return to_return


def post_to_reddit(gif_urls, rsubmission):
    if len(gif_urls) == 1:
        text = "I've converted your PGN into a gif:\n\n"
        text += "[Slow variant](" + gif_urls[0][0] + ")  \n"
        text += "[Fast variant](" + gif_urls[0][1] + ")\n\n"
    else:
        text = "I've converted your PGNs into gifs:\n\n"
        for game_urls in gif_urls:
            text += "[Slow variant](" + game_urls[0] + ")  \n"
            text += "[Fast variant](" + game_urls[1] + ")\n\n"

    text += "----\n\n*I'm a Bot. " \
            "Install the PGN Viewer addon " \
            "for [firefox](https://addons.mozilla.org/en-US/firefox/addon/reddit-pgn-viewer/) or " \
            "[chrome](https://chrome.google.com/webstore/detail/reddit-pgn-viewer/hplecpnihkigeaiobbmfnfblepiadjdh) " \
            "for a better experience. Contact /u/ganznetteigentlich for questions. " \
            "[Code](https://github.com/l3d00m/reddit-pgn-to-gif)*"
    if config.DEBUG:
        print("replying with: " + text)
    rsubmission.reply(text)
