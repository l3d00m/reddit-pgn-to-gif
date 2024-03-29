import praw
import config

reddit = praw.Reddit(client_id=config.reddit_client_id,
                     client_secret=config.reddit_client_secret,
                     user_agent='python script for converting /r/chess PGNs to GIFs by /u/ganznetteigentlich',
                     username=config.reddit_username,
                     password=config.reddit_password)

already_checked = []


class Post:
    def __init__(self, reddit_object, text, link):
        self.reddit_object = reddit_object
        self.text = text
        self.link = link


def unescape_reddit(string):
    try:
        return str(string).replace("\\[", "[") \
            .replace("\\]", "]") \
            .replace("\\_", "_") \
            .replace("\\*", "*") \
            .replace("\n\n", "\n")
    except Exception as e:
        print("Couldn't unescape reddit string: " + format(e))
        return str(string)


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
            to_return.append(Post(reddit_object=submission, text=unescape_reddit(submission.selftext), link=submission.permalink))
        already_checked.append(submission.name)

    for comment in subr.comments(limit=30):
        if comment.author is not None and comment.author.name.lower() == config.reddit_username.lower():
            continue
        if comment.name in already_checked:
            if config.DEBUG:
                print("Already checked")
            continue
        to_return.append(Post(reddit_object=comment, text=unescape_reddit(comment.body), link=comment.permalink))
        already_checked.append(comment.name)
    return to_return


def post_to_reddit(games, reddit_object):
    if len(games) == 1:
        game = games[0]
        text = "I converted your game into GIFs to make it viewable for mobile users. "
        text += "[Game GIF in different playback speeds](" + game.album_url + ")"
        if game.lichess_url is not False:
            text += " and also the [lichess analysis board](" + game.lichess_url + ")"
        text += "\n\n"
    else:
        i = 1
        text = "I converted your games into GIFs to make them viewable for mobile users: \n\n "
        for game in games:
            text += "[Gifs \(multiple playback speeds\) for game #" + str(i) + "](" + game.album_url + ")"
            if game.lichess_url is not False:
                text += " and a [lichess analysis board](" + game.lichess_url + ")"
            text += "\n\n"
            i += 1
    text += "*Hint: I only plot the mainline without any included variations.*\n"
    text += "***\n^[Code](https://github.com/l3d00m/reddit-pgn-to-gif) " \
            "^(| Ping )^@ganznetteigentlich ^(for help | " \
            "Install the **PGN Viewer addon** for) ^[firefox](https://addons.mozilla.org/en-US/firefox/addon/reddit-pgn-viewer/) " \
            "^or ^[chrome](https://chrome.google.com/webstore/detail/reddit-pgn-viewer/hplecpnihkigeaiobbmfnfblepiadjdh) ^(for the best experience.)"
    if config.DEBUG:
        print("replying with: " + repr(text))
    else:
        print("Comment submitted")
    reddit_object.reply(text)
    return True
