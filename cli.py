from quoridor.game import QuoridorGame
from quoridor.ai import random_ai_move


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
    """Prompt the user for a move using a simpler syntax."""
    while True:
        try:
            move = input(
                "Enter command (move r c | wall h r c | wall v r c | quit): "
            )
        except EOFError:
            return 'quit'
        parts = move.split()
        if not parts:
            continue
        if parts[0] in {'quit', 'exit'}:
            return 'quit'
        if parts[0] == 'move' and len(parts) == 3:
            try:
                r = int(parts[1])
                c = int(parts[2])
                game.move_pawn(r, c)
                return None
            except Exception as e:
                print('Invalid move:', e)
        elif parts[0] == 'wall' and len(parts) == 4:
            orientation = parts[1].lower()
            if orientation not in ('h', 'v'):
                print('Orientation must be h or v')
                continue
            try:
                r = int(parts[2])
                c = int(parts[3])
                game.place_wall(r, c, orientation)
                return None
            except Exception as e:
                print('Invalid wall:', e)
        else:
            print('Bad input')




def play(vs_ai=False):
    game = QuoridorGame()
    while True:
        print_board(game)
        if vs_ai and game.current_player == 1:
            random_ai_move(game)
        else:
            result = human_move(game)
            if result == 'quit':
                print('Game aborted.')
                break
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
