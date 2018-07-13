import praw
import config

reddit = praw.Reddit(client_id=config.reddit_client_id,
                     client_secret=config.reddit_client_secret,
                     user_agent='python script for converting /r/chess PGNs to GIFs by /u/ganznetteigentlich',
                     username=config.reddit_username,
                     password=config.reddit_password)

already_checked = []


def get_new_posts():
    to_return = []
    subr = reddit.subreddit(config.subreddit)

    if len(already_checked) == 0:
        print("Loading posted to")
        redditor = reddit.redditor(config.reddit_username)
        for comment in redditor.comments.new(limit=100):
            already_checked.append(comment.parent_id)

    for submission in subr.new(limit=20):
        if submission.name in already_checked:
            if config.DEBUG:
                print("Already checked")
            continue
        if submission.is_self and submission.selftext != "":
            to_return.append([submission, str(submission.selftext)])
        already_checked.append(submission.name)

    for comment in subr.comments(limit=30):
        if comment.author.name.lower() == config.reddit_username.lower():
            continue
        if comment.name in already_checked:
            if config.DEBUG:
                print("Already checked")
            continue
        to_return.append([comment, str(comment.body)])
        already_checked.append(comment.name)
    return to_return


def post_to_reddit(games, reddit_object):
    if len(games) == 1:
        text = "[Here is a gif of your PGN](" + games[0] + ")"
    else:
        i = 1
        text = "I've converted your PGNs into gifs: \n\n "
        for album_url in games:
            text += "\n\n[Gif for PGN #" + str(i) + "](" + album_url + ")\n\n"
            i += 1
    if text == "":
        print("WARNING: text was empty, should never happen")
        return False

    text += "\n\n*[Code](https://github.com/l3d00m/reddit-pgn-to-gif) | " \
            "Contact `u/ganznetteigentlich` for questions.  \n" \
            "Install the PGN Viewer addon for " \
            "[firefox](https://addons.mozilla.org/en-US/firefox/addon/reddit-pgn-viewer/) or " \
            "[chrome](https://chrome.google.com/webstore/detail/reddit-pgn-viewer/hplecpnihkigeaiobbmfnfblepiadjdh) " \
            "for a better experience.*"
    if config.DEBUG:
        print("replying with: " + text)
    else:
        print("Comment submitted")
    reddit_object.reply(text)
    return True
