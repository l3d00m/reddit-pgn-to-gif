import chess
import chess.pgn
import chess.svg
import io
import cairosvg
import imageio
from giphypop import upload
import config
import time


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
        if counter > 150:
            print("too many moves")
            break
        if config.DEBUG:
            print("Move #" + str(counter))
        board.push(move)
        images.append(position_to_image(board))
        counter += 1
    images.append(images[len(images) - 1])
    try:
        imageio.mimsave("fast.gif", images, duration=1, format="GIF")
        imageio.mimsave("slow.gif", images, duration=3, format="GIF")
    except Exception as e:
        print("error creating gif: " + format(e))
        return

    print("Generating gif took " + str(time.time() - start_time) + " s")
    try:
        gif_slow = upload(["chess"], "slow.gif")
        gif_fast = upload(["chess"], "fast.gif")
        return [gif_slow.media_url, gif_fast.media_url]
    except Exception as e:
        print("error uploading on giphy: " + format(e))
        return


def position_to_image(board):
    svg_string = chess.svg.board(board, size=400)
    # noinspection PyUnresolvedReferences
    byte_string = cairosvg.svg2png(bytestring=svg_string)
    return imageio.imread(byte_string, format="PNG")
