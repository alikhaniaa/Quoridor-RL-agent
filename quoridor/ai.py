import random
from .game import QuoridorGame


def random_ai_move(game: QuoridorGame):
    """Perform a random legal move for the current player."""
    moves = game.possible_moves()
    walls = []
    if game.remaining_walls[game.current_player] > 0:
        for r in range(game.BOARD_SIZE - 1):
            for c in range(game.BOARD_SIZE - 1):
                for o in ('h', 'v'):
                    if game._can_place_wall(r, c, o):
                        walls.append((r, c, o))
    if random.random() < 0.5 and walls:
        r, c, o = random.choice(walls)
        game.place_wall(r, c, o)
    else:
        r, c = random.choice(moves)
        game.move_pawn(r, c)
