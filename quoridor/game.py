class QuoridorGame:
    """Logic for the Quoridor board game."""

    BOARD_SIZE = 9
    WALL_COUNT = 10

    def __init__(self):
        # Player positions: (row, col)
        self.positions = {
            0: (0, self.BOARD_SIZE // 2),
            1: (self.BOARD_SIZE - 1, self.BOARD_SIZE // 2),
        }
        # Walls are stored as sets of coordinates
        # vertical_walls stores positions of the top-left cell of a vertical wall
        self.vertical_walls = set()
        # horizontal_walls stores positions of the top-left cell of a horizontal wall
        self.horizontal_walls = set()
        self.remaining_walls = {0: self.WALL_COUNT, 1: self.WALL_COUNT}
        self.current_player = 0

    def in_bounds(self, r, c):
        return 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE

    def _wall_blocks(self, from_cell, to_cell):
        fr, fc = from_cell
        tr, tc = to_cell
        if fr == tr:
            # horizontal move
            if fc < tc:
                # moving east
                return (fr, fc) in self.vertical_walls
            else:
                return (fr, tc) in self.vertical_walls
        elif fc == tc:
            # vertical move
            if fr < tr:
                return (fr, fc) in self.horizontal_walls
            else:
                return (tr, fc) in self.horizontal_walls
        return False

    def possible_moves(self, player=None):
        if player is None:
            player = self.current_player
        r, c = self.positions[player]
        opponent = 1 - player
        orow, ocol = self.positions[opponent]
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if not self.in_bounds(nr, nc):
                continue
            if self._wall_blocks((r, c), (nr, nc)):
                continue
            if (nr, nc) == (orow, ocol):
                # try to jump
                jr, jc = nr + dr, nc + dc
                if self.in_bounds(jr, jc) and not self._wall_blocks((nr, nc), (jr, jc)):
                    moves.append((jr, jc))
                else:
                    # diagonal moves
                    for ddr, ddc in [(-dc, -dr), (dc, dr)]:
                        jr, jc = nr + ddr, nc + ddc
                        if self.in_bounds(jr, jc) and not self._wall_blocks((nr, nc), (jr, jc)):
                            if not self._wall_blocks((r, c), (nr, nc)):
                                moves.append((jr, jc))
            else:
                moves.append((nr, nc))
        return moves

    def move_pawn(self, row, col):
        if (row, col) not in self.possible_moves(self.current_player):
            raise ValueError("Illegal move")
        self.positions[self.current_player] = (row, col)
        if self.is_winner(self.current_player):
            winner = self.current_player
            self.current_player = None
            return winner
        self.current_player = 1 - self.current_player
        return None

    def _can_place_wall(self, r, c, orientation):
        if orientation == 'h':
            if r < 0 or r >= self.BOARD_SIZE - 1 or c < 0 or c >= self.BOARD_SIZE - 1:
                return False
            if ((r, c) in self.horizontal_walls or (r, c + 1) in self.horizontal_walls or
                    (r, c) in self.vertical_walls):
                return False
        else:
            if r < 0 or r >= self.BOARD_SIZE - 1 or c < 0 or c >= self.BOARD_SIZE - 1:
                return False
            if ((r, c) in self.vertical_walls or (r + 1, c) in self.vertical_walls or
                    (r, c) in self.horizontal_walls):
                return False
        return True

    def place_wall(self, r, c, orientation):
        if self.remaining_walls[self.current_player] <= 0:
            raise ValueError("No walls remaining")
        if not self._can_place_wall(r, c, orientation):
            raise ValueError("Illegal wall placement")
        if orientation == 'h':
            self.horizontal_walls.add((r, c))
        else:
            self.vertical_walls.add((r, c))
        self.remaining_walls[self.current_player] -= 1
        # simple path check via BFS
        if not self._has_path(0) or not self._has_path(1):
            # rollback
            if orientation == 'h':
                self.horizontal_walls.remove((r, c))
            else:
                self.vertical_walls.remove((r, c))
            self.remaining_walls[self.current_player] += 1
            raise ValueError("Wall blocks all paths")
        self.current_player = 1 - self.current_player

    def _neighbors(self, cell):
        r, c = cell
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if self.in_bounds(nr, nc) and not self._wall_blocks((r, c), (nr, nc)):
                yield (nr, nc)

    def _has_path(self, player):
        start = self.positions[player]
        goal_row = self.BOARD_SIZE - 1 if player == 0 else 0
        from collections import deque
        seen = set([start])
        q = deque([start])
        while q:
            r, c = q.popleft()
            if r == goal_row:
                return True
            for nb in self._neighbors((r, c)):
                if nb not in seen:
                    seen.add(nb)
                    q.append(nb)
        return False

    def is_winner(self, player):
        r, _ = self.positions[player]
        if player == 0:
            return r == self.BOARD_SIZE - 1
        else:
            return r == 0
