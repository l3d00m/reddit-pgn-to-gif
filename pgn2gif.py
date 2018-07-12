import chess
import chess.pgn
import chess.svg
import io
import cairosvg
import imageio
import config
import time
import pyimgur

im = pyimgur.Imgur(config.imgur_client_id)


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
        imageio.mimsave("fast.mp4", images, duration=1, format="GIF-PIL")
        imageio.mimsave("slow.mp4", images, duration=3, format="GIF-PIL")
    except Exception as e:
        print("error creating gif: " + format(e))
        return

    print("Generating gif took " + str(time.time() - start_time) + " s")
    try:
        gif_slow = im.upload_image("slow.mp4", title="/r/chess pgn to video")
        gif_fast = im.upload_image("fast.mp4", title="/r/chess pgn to video")
        return [gif_slow.link, gif_fast.link]
    except Exception as e:
        print("error uploading on imgur: " + format(e))
        return


def position_to_image(board):
    svg_string = chess.svg.board(board, size=400)
    # noinspection PyUnresolvedReferences
    byte_string = cairosvg.svg2png(bytestring=svg_string)
    return imageio.imread(byte_string, format="PNG")
