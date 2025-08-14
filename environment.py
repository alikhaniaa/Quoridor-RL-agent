"""
    Structure of input(obs) and outputs(action space) and gymnasium integration
"""
import gymnasium as gym
from gymnasium import spaces
import numpy as np
from typing import Optional, Tuple, List, Dict, Any

from engine import GameState

#Gym env for Quoridor game and a wrapper for GameState
class QuoridorEnv(gym.Env):
    def __init__(self, board_size: int = 9, walls_per_player: int = 10):
        super().__init__()
        self.board_size = board_size
        self.walls_per_player = walls_per_player
        
        self.game_state: GameState = GameState(board_size, walls_per_player)
        
        self.observation_space = (spaces.Box(
            low = 0.0,
            high = 1.0, 
            shape = (6, self.board_size, self.board_size),
            dtype = np.float32
        ))