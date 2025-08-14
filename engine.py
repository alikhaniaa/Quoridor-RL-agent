"""
    Enfore the rules and represent the complete state of a Quoridor game.
    Core logic engine of AI and UI
"""
from collections import deque
from typing import Tuple, List, Optional
import copy

class GameState:
    def __init__(self, board_size: int = 9, walls_per_player: int = 10):
        self.board_size: int = board_size
        self.walls_per_player: int = walls_per_player
        
        #Pwan State
        self.pawn_pos: List[Tuple[int, int]] = [
            (0, self.board_size // 2),
            (self.board_size - 1, self.board_size // 2)
        ]
        self.player_goals: List[int] = [self.board_size - 1, 0]
        
        #Wall State
        wall_grid_size = self.board_size - 1
        self.horizontal_walls: List[List[bool]] = [[False] * wall_grid_size for _ in range(wall_grid_size)]
        self.vertical_walls: List[List[bool]] = [[False] * wall_grid_size for _ in range(wall_grid_size)]
        self.walls_left: List[int] = self.walls_per_player, self.walls_per_player
        
        #Turns and game status
        self.current_player: int = 0
        self.game_over: bool = False
        self.winner: Optional[int] = None
        
    #Check if wall placed correctly(two adjusted squeares)
    def _is_wall_between(self, r1: int, c1: int, r2: int, c2: int) -> bool:
        if r1 == r2: #horizontal move
            c = min(c1, c2)
            if self.vertical_walls[r1][c]:
                return True
            if r1 > 0 and self.vertical_walls[r1 - 1][c]:
                return True
        elif c1 == c2: #vertical move
            r = min(r1, r2)
            if self.horizontal_walls[r][c1]:
                return True
            if c1 > 0 and self.horizontal_walls[r][v1 - 1]:
                return True
        return False
        #TODO don't know if I need to limit the placement instead of aknowledging right or wrong move(for RL optimization)

    #Check if the player can move
    def _is_jump_blocked(self, r1: int, c1: int, r2: int, c2: int) -> bool:
        return self._is_wall_between(r1, c1, r2, c2)
        
    ## **TODO checking if player is completely blocked.
    # usign a Breadth-First search method(since it's a simple grid search probably the best way)
    # TODO should think about other ways later to find any more optimized solution
    def _is_path_blocked(self) -> bool:
        def _bfs_path_exists(start_pos: Tuple[int, int], goal_row: int) -> bool:
            queue = deque([start_pos])
            visited = {start_pos}
            
            while queue:
                r, c = queue.popleft()
                
                if r == goal_row:
                    return True
                
                #checking all 4 neighbords
                for dr, dc in [(0,1), (0, -1), (1, 0), (-1,0)]:
                    nr, nc = r + dr, c + dc
                    
                    #checking if neighbour is reachable
                    if 0 <= nr < self.board_size and 0 <= nc < self.board_size:
                        if (nr, nc) not in visited and not self._is_wall_between(r, c, nr, nc):
                            visited.add((nr, nc))
                            queue.append((nr, nc))
                            
            return False
        
        player0_has_path = _bfs_path_exists(self.pawn_pos[0], self.player_goals[0])
        player1_had_path = _bfs_path_exists(self.pawn_pos[1], self.player_goals[1])
        
        return not player0_has_path or not player1_had_path
    
    #List of legal wall placements
    def get_legal_walls(self) -> List[Tuple[str, int, int]]:
        if self.walls_left[self.current_player] == 0:
            return[]
        
        legal_placements = []
        wall_grid_size = self.board_size - 1
        
        for r in range(wall_grid_size):
            for c in range(wall_grid_size):
                #horizontal placements
                if not self.horizontal_walls[r][c] and not self.vertical_walls[r][c]:
                    h_adj_valid = True
                    if c > 0 and self.horizontal_walls[r][c - 1]: h_adj_valid = False
                    if c < wall_grid_size - 1 and self.horizontal_walls[r][c + 1]: h_adj_valid = False
                    
                    if h_adj_valid:
                        self.horizontal_walls[r][c] = True
                        if not self._is_path_blocked():
                            legal_placements.append(('H', r, c))
                        self.horizontal_walls[r][c] = False
                        
                #vertical placements
                if not self.vertical_walls[r][c] and not self.horizontal_walls[r][c]:
                    v_adj_valid = True
                    if r > 0 and self.vertical_walls[r - 1][c]: v_adj_valid = False
                    if r < wall_grid_size - 1 and self.vertical_walls[r + 1][c]: v_adj_valid = False
                    
                    if v_adj_valid:
                        self.vertical_walls[r][c] = True
                        if not self._is_path_blocked():
                            legal_placements.append(('v', r, c))
                        self.vertical_walls[r][c] = False
            
            return legal_placements           
    
    
    
    #List of legal pawn moves
    def get_legal_moves(self) -> List[Tuple[int, int]]:
        legal_moves = []
        r, c = self.pawn_pos[self.current_player]
        opponent_pos = self.pawn_pos[1 - self.current_player]
        
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            if not (0 <= nr < self.board_size and 0 <= nc < self.board_size):
                continue
            
            if self._is_wall_between(r, c, nr, nc):
                continue
            
            if (nr, nc) == opponent_pos:
                #jumping logics(we have 2 type of jumps. if facing each other jump 2 blocks, if second block is closed it can jump diagonally)
                jr, jc = nr + dr, nc + dc
                
                if 0 <= jr < self.board_size and 0 <= jc < self.board_size and not self._is_jump_blocked(nr, nc, jr, jc):
                    legal_moves.append((jr, jc))
                else: 
                    #diagonal jump
                    if dr == 0:
                        if r > 0 and not self._is_wall_between(nr, nc, nr - 1, nc):
                            legal_moves.append((nr - 1, nc)) # up diagonal
                        if r < self.board_size - 1 and not self._is_wall_between(nr, nc, nr + 1, nc):
                            legal_moves.append((nr + 1, nc)) # downl diagonal
                        else: 
                            if c > 0 and not self._is_wall_between(nr, nc, nr, nc - 1):
                                legal_moves.append((nr, nc - 1)) #left diagonal
                            if c < self.board_size - 1 and not self._is_wall_between(nr, nc, nr, nc + 1):
                                legal_moves.append((nr, nc + 1)) #right diagonal
            else:
                legal_moves.append((nr, nc))
                
        return legal_moves    
    
    #Deep copy of current game state
    def clone(self) -> 'GameState':
        new_state = GameState(self.board_size, self.walls_per_player)
        new_state.pawn_pos = self.pawn_pos[:]
        new_state.horizontal_walls = copy.deepcopy(self.horizontal_walls)
        new_state.vertical_walls = copy.deepcopy(self.vertical_walls)
        new_state.walls_left = self.walls_left[:]
        new_state.current_player = self.current_player
        new_state.game_over = self.game_over
        new_state.winner = self.winner
        return new_state
        
    #Pawn move
    def move_pawn(self, target_pos: Tuple[int, int]) -> bool:
        self.pawn_pos[self.current_player] = target_pos
        
        #check for win
        if target_pos[0] == self.player_goals[self.current_player]:
            self.game_over = True
            self.winner = self.current_player
            return True
        
        self.current_player = 1 - self.current_player
        return True
    
    #Wall placement
    def place_wall(self, orientation: str, r: int, c: int) -> bool:
        self.walls_left[self.current_player] -= 1
        
        if orientation == 'h':
            self.horizontal_walls[r][c] = True
        else:
            self.vertical_walls[r][c] = True
            
        self.current_player = 1 - self.current_player
        return True