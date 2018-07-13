import chess
import chess.pgn
import chess.svg
import io
import cairosvg
import imageio
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
        return
    board = game.board()
    images = [position_to_image(board)]
    counter = 0
    for move in game.main_line():
        if counter > 250:
            print("too many moves")
            break
        if config.DEBUG:
            print("Move #" + str(counter))
        board.push(move)
        images.append(position_to_image(board))
        counter += 1
    images.append(images[len(images) - 1])
    try:
        imageio.mimsave("fast.gif", images, duration=1)
        imageio.mimsave("normal.gif", images, duration=2)
        imageio.mimsave("slow.gif", images, duration=4)
    except Exception as e:
        if config.DEBUG:
            raise
        else:
            print("error creating gif: " + format(e))
            return

    print("Generating gif took " + str(time.time() - start_time) + " s")
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
        else:
            print("error uploading on imgur: " + format(e))
            return


def position_to_image(board):
    svg_string = chess.svg.board(board, size=400)
    # noinspection PyUnresolvedReferences
    byte_string = cairosvg.svg2png(bytestring=svg_string)
    return imageio.imread(byte_string, format="PNG")
