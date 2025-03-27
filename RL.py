import numpy as np
import random
from hashlib import sha1

class QLearningAgent:
    """
    A Q-learning agent for reinforcement learning in the Othello game.
    """

    def __init__(self, state_size, action_size, learning_rate=0.1, discount_factor=0.95, epsilon=0.1):
        """
        Initialize the Q-learning agent.

        Args:
            state_size (int): The size of the state space.
            action_size (int): The size of the action space.
            learning_rate (float): The learning rate for Q-value updates.
            discount_factor (float): The discount factor for future rewards.
            epsilon (float): The exploration rate for the epsilon-greedy policy.
        """
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.q_table = {}

    def get_state_key(self, state):
        """
        Convert a state array to a hashable tuple for use as a dictionary key.

        Args:
            state (numpy.array): The current state of the game.

        Returns:
            tuple: A hashable representation of the state.
        """
        state_bytes = state.tobytes()
        state_hash = sha1(state_bytes).hexdigest()
        return state_hash

    def get_action(self, state, valid_moves):
        """
        Choose an action using an epsilon-greedy policy.

        Args:
            state (numpy.array): The current state of the game.
            valid_moves (list): A list of valid moves in the current state.

        Returns:
            int: The chosen action.
        """
        state_key = self.get_state_key(state)
        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros(self.action_size)

        if np.random.rand() < self.epsilon:
            return random.choice(valid_moves)
        
        valid_q_values = [self.q_table[state_key][action] for action in valid_moves]
        return valid_moves[np.argmax(valid_q_values)]

    def update(self, state, action, reward, next_state, done):
        """
        Update the Q-value for a state-action pair.

        Args:
            state (numpy.array): The current state.
            action (int): The action taken.
            reward (float): The reward received.
            next_state (numpy.array): The resulting state after taking the action.
            done (bool): Whether the episode has ended.
        """
        state_key = self.get_state_key(state)
        next_state_key = self.get_state_key(next_state)

        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros(self.action_size)
        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = np.zeros(self.action_size)

        current_q = self.q_table[state_key][action]
        if done:
            target_q = reward
        else:
            target_q = reward + self.discount_factor * np.max(self.q_table[next_state_key])
        self.q_table[state_key][action] += self.learning_rate * (target_q - current_q)
        