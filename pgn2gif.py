import cairosvg
import chess
import chess.pgn
import chess.svg
import io
import imageio
from giphypop import upload
import config


def convert_pgn_to_gif(pgn):
    pgn_file = io.StringIO(str(pgn))
    game = chess.pgn.read_game(pgn_file)
    board = game.board()
    images = [position_to_image(board)]
    for move in game.main_line():
        board.push(move)
        images.append(position_to_image(board))
    images.append(images[len(images) - 1])
    imageio.mimsave('fast.gif', images, duration=1)
    imageio.mimsave('slow.gif', images, duration=4)
    gif_slow = upload(["chess", "r/chess"], 'slow.gif', api_key=config.giphy_key)
    gif_fast = upload(["chess", "r/chess"], 'fast.gif', api_key=config.giphy_key)
    return [gif_slow.media_url, gif_fast.media_url]


def position_to_image(board):
    svg_string = chess.svg.board(board)
    # noinspection PyUnresolvedReferences
    cairosvg.svg2png(bytestring=svg_string, write_to="output.png")
    return imageio.imread("output.png")
