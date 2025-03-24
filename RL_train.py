import numpy as np
import random
import pickle
from HexOthello import ThreePlayerOthello

class OthelloQLearningAgent:
    def __init__(self, state_size, action_size, epsilon=1.0, decay_rate=0.9998, gamma=0.9):
        self.state_size = state_size
        self.action_size = action_size
        self.epsilon = epsilon
        self.decay_rate = decay_rate
        self.gamma = gamma
        self.q_table = {}
        self.num_updates = {}
        
    def get_state_key(self, state):
        # Convert numpy array to tuple for dictionary key
        return tuple(state.flatten())
        
    def get_action(self, state, valid_actions):
        state_key = self.get_state_key(state)
        
        # Initialize Q-values for new state
        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros(self.action_size)
            self.num_updates[state_key] = np.zeros(self.action_size)
        
        # Epsilon-greedy action selection
        if np.random.random() < self.epsilon:
            return random.choice(valid_actions)
        else:
            # Select best action among valid actions
            valid_q_values = [self.q_table[state_key][action] for action in valid_actions]
            max_value_index = np.argmax(valid_q_values)
            return valid_actions[max_value_index]
    
    def update(self, state, action, reward, next_state, done):
        state_key = self.get_state_key(state)
        next_state_key = self.get_state_key(next_state)
        
        # Initialize Q-values for new states
        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros(self.action_size)
            self.num_updates[state_key] = np.zeros(self.action_size)
        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = np.zeros(self.action_size)
            self.num_updates[next_state_key] = np.zeros(self.action_size)
        
        # Update counter for this state-action pair
        self.num_updates[state_key][action] += 1
        
        # Calculate dynamic learning rate (eta)
        eta = 1.0 / (1.0 + self.num_updates[state_key][action])
        
        # Calculate target value
        if done:
            target = reward
        else:
            target = reward + self.gamma * np.max(self.q_table[next_state_key])
        
        # Update Q-value
        self.q_table[state_key][action] = (1 - eta) * self.q_table[state_key][action] + eta * target
    
    def decay_epsilon(self):
        self.epsilon *= self.decay_rate
        
    def save_q_table(self, filename):
        with open(filename, 'wb') as handle:
            pickle.dump(self.q_table, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    def load_q_table(self, filename):
        with open(filename, 'rb') as handle:
            self.q_table = pickle.load(handle)

    def train_rl_agent(num_episodes=1000, gamma=0.9, epsilon=1.0, decay_rate=0.99):
        # Initialize the game and agent
        game = ThreePlayerOthello()
        agent = OthelloQLearningAgent(state_size=15*22, action_size=15*22, 
                                    epsilon=epsilon, decay_rate=decay_rate, gamma=gamma)

        total_rewards = []
        rl_wins = 0
        
        for episode in range(num_episodes):
            game.reset()
            done = False
            episode_reward = 0
            
            while not done:
                current_player = game.players[game.current_player_index]
                
                if current_player == "A ":  # Random player
                    moves = game.valid_moves("A ")
                    if moves:
                        move = random.choice(moves)
                        game.make_move(move[0], move[1], "A ")
                    
                elif current_player == "B ":  # First-move player
                    moves = game.valid_moves("B ")
                    if moves:
                        move = moves[0]
                        game.make_move(move[0], move[1], "B ")
                    
                else:  # RL agent (player C)
                    moves = game.valid_moves("C ")
                    if not moves:
                        game.current_player_index = (game.current_player_index + 1) % 3
                        continue
                    
                    # Get current state
                    state = np.array([game.get_numeric_state()])
                    
                    # Convert moves to actions
                    valid_actions = [row * 22 + col for row, col in moves]
                    
                    # Get action from agent
                    action = agent.get_action(state, valid_actions)
                    
                    # Convert action back to move
                    row, col = divmod(action, 22)
                    
                    # Make the move
                    game.make_move(row, col, "C ")
                    
                    # Get reward
                    reward = game.get_reward("C ")
                    episode_reward += reward
                    
                    # Get next state
                    next_state = np.array([game.get_numeric_state()])
                    
                    # Check if game is over
                    done = game.game_over()
                    
                    # Update Q-values
                    agent.update(state, action, reward, next_state, done)
                
                # Move to next player
                game.current_player_index = (game.current_player_index + 1) % 3
                
                # Check if game is over
                if game.game_over():
                    done = True
            
            total_rewards.append(episode_reward)

            if game.count_disks()["C "] == max(game.count_disks().values()):
                rl_wins += 1

            # Decay epsilon after each episode
            agent.decay_epsilon()
            
            # Print progress
            # if episode % 100 == 0:
            #     print(f"Episode {episode}/{num_episodes}, Epsilon: {agent.epsilon:.4f}")

            if episode > 0 and episode % 100 == 0:
                avg_reward = sum(total_rewards[-100:]) / min(len(total_rewards), 100)
                print(f"Episode {episode}/{num_episodes}, Epsilon: {agent.epsilon:.4f}, Avg Reward: {avg_reward:.2f}")
        
        print(f"RL Agent Win Rate: {rl_wins / num_episodes * 100:.2f}%")

        # Save the trained agent
        agent.save_q_table("othello_q_table.pickle")
        return agent

if __name__ == "__main__":
    agent = OthelloQLearningAgent.train_rl_agent(num_episodes=1000, gamma=0.9, epsilon=1, decay_rate=0.996)