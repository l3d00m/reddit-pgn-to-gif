import chess
import chess.pgn
import chess.svg
import io
import imageio
import cairosvg
import config
import time
import pyimgur

im = pyimgur.Imgur(client_id=config.imgur_client_id, client_secret=config.imgur_client_secret)
im.refresh_token = config.imgur_refresh_token


def convert_pgn_to_gif(pgn):
    start_time = time.time()
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
    board = game.board()
    images = [position_to_image(board)]
    counter = 0
    for move in game.mainline_moves():
        if counter > 500:
            print("too many moves")
            break
        if config.DEBUG:
            print("Move #" + str(counter + 1))
        board.push(move)
        image = position_to_image(board)
        if image is False:
            return False
        images.append(image)
        counter += 1
    images.append(images[len(images) - 1])
    result = create_gifs(images)
    if result is False:
        return False
    print("Generating gif took " + str(time.time() - start_time) + " s")
    return upload_to_imgur()


def create_gifs(images):
    try:
        imageio.mimsave("fast.gif", images, duration=1)
        imageio.mimsave("normal.gif", images, duration=2)
        imageio.mimsave("slow.gif", images, duration=4)
        return True
    except Exception as e:
        if config.DEBUG:
            raise
        print("error creating gif: " + format(e))
    return False


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


def position_to_image(board):
    try:
        svg_string = chess.svg.board(board, size=400)
        byte_string = cairosvg.svg2png(bytestring=svg_string)
        return imageio.imread(byte_string, format="PNG")
    except Exception as e:
        if config.DEBUG:
            raise
        print("error converting board to image: " + format(e))
    return False
