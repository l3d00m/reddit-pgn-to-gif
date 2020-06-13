import chess
import chess.pgn
import io
import config
import time
import pyimgur
import json
import requests

im = pyimgur.Imgur(client_id=config.imgur_client_id, client_secret=config.imgur_client_secret)
im.refresh_token = config.imgur_refresh_token
lila_gif_url = "http://127.0.0.1:6175/game.gif"


def convert_pgn_to_gif(pgn):
    start_time = time.time()
    game = parse_pgn_to_game(pgn)
    if game is False:
        raise ValueError("Could not parse game")
    request = create_lila_gif_request(game)
    if request is False:
        raise ValueError("Could not create lila gif request from moves")

    #result = create_gifs(frames)
    # if result is False:
    #    return False
    #print("Generating gif took " + str(time.time() - start_time) + " s")
    # return upload_to_imgur()


def create_lila_gif_request(game):
    board = game.board()
    frames = list()
    last_move = False
    for i, move in enumerate(game.mainline_moves()):
        frame = {}
        if i > 1000:
            print("Too many moves")
            break
        if config.DEBUG:
            print("Move #" + str(i))
        if last_move is not False:
            frame["lastMove"] = last_move

        frame["fen"] = board.fen()
        frame["check"] = board.is_check()
        last_move = move.uci()
        board.push(move)
        frames.append(frame)
    req_body = {}
    player_white = game.headers["White"]
    player_black = game.headers["Black"]
    if player_white != "?":
        req_body["white"] = player_white
    if player_black != "?":
        req_body["black"] = player_black
    if game.headers.get("StartFlipped", False) == "1":
        req_body["orientation"] = "black"
    req_body["comment"] = "https://reddit.com/u/PGNtoGIF"
    req_body["frames"] = frames
    return req_body


def make_lila_gif_request(req_body):
    req_body["delay"] = 800
    req_fast = json.dumps(req_body)
    req_body["delay"] = 2000
    req_slow = json.dumps(req_body)
    response_slow = requests.post(lila_gif_url, data=req_slow)
    if response_slow.ok:
        with open("slow.jpg", 'wb') as f:
            f.write(response_slow.content)
    response_fast = requests.post(lila_gif_url, data=req_fast)
    if response_fast.ok:
        with open("fast.jpg", 'wb') as f:
            f.write(response_fast.content)


def parse_pgn_to_game(pgn):
    pgn_file = io.StringIO(str(pgn))
    game = chess.pgn.read_game(pgn_file)
    if game is None:
        print("No valid PGN detected")
        return False
    if len(game.errors) > 0:
        print("errors detected, aborting")
        for error in game.errors:
            print(error)
        return False
    return game


def upload_to_imgur():
    try:
        im.refresh_access_token()
        gif_slow = im.upload_image("slow.gif", title="Slow speed")
        gif_normal = im.upload_image("normal.gif", title="Normal speed")
        gif_fast = im.upload_image("fast.gif", title="Fast speed")
        album = im.create_album("/r/chess PGN gifs", images=[gif_fast.id, gif_normal.id, gif_slow.id])
        return album.link
    except Exception as e:
        if config.DEBUG:
            raise
        print("error uploading on imgur: " + format(e))
    return False


if __name__ == "__main__":
    convert_pgn_to_gif(
        "[Event \"Rated Bullet game\"]\r\n[StartFlipped \"1\"]\r\n[Date \"2020.04.21\"]\r\n[Round \"-\"]\r\n[Black \"someone\"]\r\n[Result \"0-1\"]\r\n[UTCDate \"2020.04.21\"]\r\n[UTCTime \"08:39:28\"]\r\n[WhiteElo \"1411\"]\r\n[BlackElo \"1436\"]\r\n[WhiteRatingDiff \"-10\"]\r\n[BlackRatingDiff \"+6\"]\r\n[Variant \"Standard\"]\r\n[TimeControl \"60+0\"]\r\n[ECO \"B45\"]\r\n[Opening \"Sicilian Defense: Paulsen Variation, Normal Variation\"]\r\n[Termination \"Time forfeit\"]\r\n[Annotator \"lichess.org\"]\r\n\r\n1. e4 e6 2. Nf3 c5 3. Nc3 Nc6 4. d4 cxd4 5. Nxd4 { B45 Sicilian Defense: Paulsen Variation, Normal Variation } g6 6. Bd3 Bg7 7. Be3 Nxd4 8. Bxd4 Bxd4 9. Bb5 Bg7 10. Qd2 Ne7 11. O-O-O O-O 12. Bxd7 Bxd7 13. Qxd7 Qxd7 14. Rxd7 Nc6 15. Rxb7 Na5 16. Rb5 Nc4 17. Rc5 Bxc3 18. Rxc4 Bg7 19. Rd1 Rfc8 20. Rxc8+ Rxc8 21. f4 e5 22. f5 gxf5 23. exf5 Bh6+ 24. Kb1 Kg7 25. h4 Kf6 26. g4 Bf4 27. g5+ Kg7 28. f6+ Kg6 29. Rf1 Rc4 30. Re1 Rd4 31. c3 Rd2 { Black wins on time. } 0-1")
