# Three-Player Othello (RL Agent)

This project implements a three-player variant of the classic Othello board game with a Q-learning agent and a hexagonal board. 

## Overview

- **HexBoard.py**  
  Generates a board using configurable parameters.

- **HexOthello.py**  
  Implements the game logic for three-player Othello, including move validation, board state updates, and reward computation.

- **RL_train.py**  
  Contains the Q-learning agent (`OthelloQLearningAgent`) and a training routine (`train_rl_agent`). Trains a model through repeated gameplay, updates Q-table, and saves it.

- **HexGUI.py**  
  Provides a Tkinter GUI to visualize and play the game. Loads the trained Q-table to let the agent play as player **C**.

## Requirements

- Python 3.x
- NumPy  
- SciPy  
- Tkinter  
- pickle  
- random  
- hashlib  

## Usage

1. **Train the agent (optional, if you want a new Q-table):**
   ```bash
   python RL_train.py
   ```

2. **Run the GUI to play or watch the agent:**
   ```bash
   python HexGUI.py
   ```

The agent is trained to control player **C**, with players **A** and **B** using random or fixed strategies. Adjust hyperparameters (epsilon, decay_rate, gamma, etc.) in `RL_train.py` or in the `OthelloQLearningAgent` constructor as desired.

## Project Structure

```
Main_Project/
├── HexBoard.py
├── HexGUI.py
├── HexOthello.py
├── RL_train.py
└── README.md
```
