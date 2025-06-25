import random
from quoridor.game import QuoridorGame


def print_board(game):
    board = [['.' for _ in range(game.BOARD_SIZE)] for _ in range(game.BOARD_SIZE)]
    r0, c0 = game.positions[0]
    r1, c1 = game.positions[1]
    board[r0][c0] = 'A'
    board[r1][c1] = 'B'
    for r, c in game.horizontal_walls:
        board[r][c] = '='
    for r, c in game.vertical_walls:
        board[r][c] = '|'
    print('\n'.join(' '.join(row) for row in board))
    print()


def human_move(game):
    while True:
        try:
            move = input('Enter move (e.g., m r c or wh r c or wv r c): ')
        except EOFError:
            return None
        parts = move.split()
        if not parts:
            continue
        if parts[0] == 'm' and len(parts) == 3:
            try:
                r = int(parts[1])
                c = int(parts[2])
                game.move_pawn(r, c)
                break
            except Exception as e:
                print('Invalid move:', e)
        elif parts[0] in ('wh', 'wv') and len(parts) == 3:
            try:
                r = int(parts[1])
                c = int(parts[2])
                orientation = 'h' if parts[0] == 'wh' else 'v'
                game.place_wall(r, c, orientation)
                break
            except Exception as e:
                print('Invalid wall:', e)
        else:
            print('Bad input')


def random_ai_move(game):
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


def play(vs_ai=False):
    game = QuoridorGame()
    while True:
        print_board(game)
        if vs_ai and game.current_player == 1:
            random_ai_move(game)
        else:
            human_move(game)
        if game.current_player is None:
            winner = 1 - game.current_player
            print(f'Player {winner} wins!')
            break


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Play Quoridor.')
    parser.add_argument('--ai', action='store_true', help='Play against random AI')
    args = parser.parse_args()
    play(vs_ai=args.ai)
