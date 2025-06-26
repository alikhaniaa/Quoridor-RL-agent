import gymnasium as gym
from gymnasium import spaces
import numpy as np

from .game import QuoridorGame


class QuoridorEnv(gym.Env):
    """Gymnasium environment for Quoridor."""

    metadata = {"render_modes": ["human"], "render_fps": 4}

    def __init__(self, render_mode=None):
        super().__init__()
        self.game = QuoridorGame()
        self.render_mode = render_mode
        # action space: 81 moves + 2*(8*8) wall placements
        self.action_space = spaces.Discrete(81 + 2 * 8 * 8)
        # observation: board state
        # 3 channels: player positions and walls
        self.observation_space = spaces.Box(0, 1, shape=(3, 9, 9), dtype=np.int8)

    def _encode(self):
        obs = np.zeros((3, 9, 9), dtype=np.int8)
        r0, c0 = self.game.positions[0]
        r1, c1 = self.game.positions[1]
        obs[0, r0, c0] = 1
        obs[1, r1, c1] = 1
        for r, c in self.game.horizontal_walls:
            obs[2, r, c] = 1
        for r, c in self.game.vertical_walls:
            obs[2, r, c] = 1
        return obs

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.game = QuoridorGame()
        return self._encode(), {}

    def step(self, action):
        if action < 81:
            row = action // 9
            col = action % 9
            try:
                winner = self.game.move_pawn(row, col)
            except ValueError:
                reward = -1.0
                done = True
                return self._encode(), reward, done, False, {}
        else:
            idx = action - 81
            orientation = 'h' if idx < 64 else 'v'
            idx = idx % 64
            row = idx // 8
            col = idx % 8
            try:
                self.game.place_wall(row, col, orientation)
            except ValueError:
                reward = -1.0
                done = True
                return self._encode(), reward, done, False, {}
            winner = None
        if winner is not None:
            reward = 1.0
            done = True
        else:
            reward = 0.0
            done = False
        return self._encode(), reward, done, False, {}

    def render(self):
        if self.render_mode != "human":
            return
        board = [['.' for _ in range(9)] for _ in range(9)]
        r0, c0 = self.game.positions[0]
        r1, c1 = self.game.positions[1]
        board[r0][c0] = 'A'
        board[r1][c1] = 'B'
        for r, c in self.game.horizontal_walls:
            board[r][c] = '='
        for r, c in self.game.vertical_walls:
            board[r][c] = '|'
        print("\n".join(" ".join(row) for row in board))

    def close(self):
        pass
