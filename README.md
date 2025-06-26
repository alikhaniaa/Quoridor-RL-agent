# Quoridor RL Agent

This repository contains a simple implementation of the board game **Quoridor** along with a `gymnasium` compatible environment. It allows two human players to play against each other or a single player to play against a very basic random AI. The environment will be useful for training reinforcement learning agents later.

## Playing the Game

Run the CLI in two-player mode:

```bash
python cli.py
```

Run the CLI against a random opponent:

```bash
python cli.py --ai
```

Moves are entered using a simpler syntax:

- `move ROW COL` – move your pawn to a cell
- `wall h ROW COL` – place a horizontal wall with its top-left corner at `(ROW, COL)`
- `wall v ROW COL` – place a vertical wall with its top-left corner at `(ROW, COL)`

Rows and columns are 0-indexed.

Alternatively you can use a basic GUI:

```bash
python gui.py            # human vs. human
python gui.py --ai       # play against the random AI
```

## Using the Environment

```python
import gymnasium as gym
from quoridor.env import QuoridorEnv

env = QuoridorEnv()
obs, info = env.reset()
```

Actions are encoded as integers. The first 81 actions correspond to moving the pawn to a specific cell. The remaining actions correspond to wall placements.
