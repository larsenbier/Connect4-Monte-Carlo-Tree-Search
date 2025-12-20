# Connect4-Monte-Carlo-Tree-Search

Using Monte Carlo Tree Search, we achieve high-performance on generalized Connect4 against a human player. The environment, game, and search AI are all coded in python, including an interactive UI that enables a human to change the AI’s skill level and play against it. The UI only allows for traditional Connect4, however the underlying implementations allows for playing on a board of size n x m with the goal of connecting k chips. We refer to this general game setup as ConnectN.

# Playing Against the AI

`Connect4_MCTS.exe` is built from `main.py` using PyInstaller and requires no prior setup to play!

If you are a skeptical of the executable, you can simply place `main.py`, `search.py`, `tree.py`, and `env.py` in a folder together, then run `main.py` from any python environment with the `readchar` package installed.

# Files

### `main.py`

Contains the main function handling the UI and gameplay between a human player and the AI.

### `env.py`

Contains the state-space representation of ConnectN (internally called `State`), along with the functions to determine the available actions at a given state and how to apply actions to a state.

### `search.py`

Contains the Monte Carlo tree search function. For memory efficiency, nodes in the search tree only contain the action (an integer representing the column to play in), and during playout states are reconstructed by following the history of actions along a branch.

### `tree.py`

A simple `Node` class used for constructing the search tree.

### `Connect4_MCTS.exe`

The executable `Connect4_MCTS.exe` was built using PyInstaller on `main.py`. 
