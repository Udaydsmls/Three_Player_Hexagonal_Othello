import numpy as np
import random
import pickle
from HexOthello import ThreePlayerOthello
from scipy.sparse import dok_matrix
from hashlib import sha256

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
        state_bytes = state.tobytes()
        state_hash = sha256(state_bytes).hexdigest()
        return state_hash
        
    def get_action(self, state, valid_actions):
        state_key = self.get_state_key(state)
        
        if state_key not in self.q_table:
            self.q_table[state_key] = dok_matrix((1, self.action_size), dtype=np.float64)
            self.num_updates[state_key] = np.zeros(self.action_size)
        
        if np.random.random() < self.epsilon:
            return random.choice(valid_actions)
        else:
            q_values = self.q_table[state_key].todense().A1
            valid_q_values = [q_values[action] for action in valid_actions]
            max_value_index = np.argmax(valid_q_values)
            return valid_actions[max_value_index]
    
    def update(self, state, action, reward, next_state, done):
        state_key = self.get_state_key(state)
        next_state_key = self.get_state_key(next_state)
        
        if state_key not in self.q_table:
            self.q_table[state_key] = dok_matrix((1, self.action_size), dtype=np.float64)
            self.num_updates[state_key] = np.zeros(self.action_size)
        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = dok_matrix((1, self.action_size), dtype=np.float64)
            self.num_updates[next_state_key] = np.zeros(self.action_size)
        
        self.num_updates[state_key][action] += 1
        eta = 1.0 / (1.0 + self.num_updates[state_key][action])

        current_value = self.q_table[state_key].get((0, action), 0.0)
        
        if done:
            target = reward
        else:
            next_q_dense = self.q_table[next_state_key].todense().A1
            target = reward + self.gamma * np.max(next_q_dense)
        
        new_value = (1 - eta) * current_value + eta * target
        self.q_table[state_key][0, action] = new_value
    
    def decay_epsilon(self):
        self.epsilon *= self.decay_rate
        
    def save_q_table(self, filename):
        with open(filename, 'wb') as handle:
            pickle.dump(self.q_table, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    def load_q_table(self, filename):
        with open(filename, 'rb') as handle:
            self.q_table = pickle.load(handle)

    def train_rl_agent(num_episodes=1000, gamma=0.9, epsilon=1.0, decay_rate=0.99):
        game = ThreePlayerOthello()
        agent = OthelloQLearningAgent(state_size=13*19, action_size=13*19, 
                                    epsilon=epsilon, decay_rate=decay_rate, gamma=gamma)

        total_rewards = []
        rl_wins = 0
        
        for episode in range(num_episodes):
            game.reset()
            done = False
            episode_reward = 0
            
            while not done:
                current_player = game.players[game.current_player_index]
                
                if current_player == "A ":  
                    moves = game.valid_moves("A ")
                    if moves:
                        move = random.choice(moves)
                        game.make_move(move[0], move[1], "A ")
                    
                # elif current_player == "B ":  
                #     moves = game.valid_moves("B ")
                #     if moves:
                #         move = moves[0]
                #         game.make_move(move[0], move[1], "B ")

                elif current_player == "B ":
                    moves = game.valid_moves("B ")
                    
                    if moves:
                        best_move = None
                        max_flips = -1
                        
                        for move in moves:
                            r, c = move
                            temp_board = [row[:] for row in game.board]
                            game.make_move(r, c, "B ")
                            
                            flipped_pieces = sum(row.count("B ") for row in game.board) - sum(row.count("B ") for row in temp_board)
                            
                            game.board = temp_board 
                            
                            if flipped_pieces > max_flips:
                                max_flips = flipped_pieces
                                best_move = move
                        
                        if best_move:
                            game.make_move(best_move[0], best_move[1], "B ")
                    
                else:
                    moves = game.valid_moves("C ")
                    if not moves:
                        game.current_player_index = (game.current_player_index + 1) % 3
                        continue
                    
                    state = np.array([game.get_numeric_state("C ")])
                    valid_actions = [row * 19 + col for row, col in moves]
                    action = agent.get_action(state, valid_actions)
                    row, col = divmod(action, 19)
                    game.make_move(row, col, "C ")
                    reward = game.get_reward("C ")
                    episode_reward += reward
                    next_state = np.array([game.get_numeric_state("C ")])
                    done = game.game_over()
                    agent.update(state, action, reward, next_state, done)
                
                game.current_player_index = (game.current_player_index + 1) % 3

                if game.game_over():
                    done = True
            
            total_rewards.append(episode_reward)

            if game.count_disks()["C "] == max(game.count_disks().values()):
                rl_wins += 1

            agent.decay_epsilon()

            if episode > 0 and episode % 100 == 0:
                avg_reward = sum(total_rewards[-100:]) / min(len(total_rewards), 100)
                print(f"Episode {episode}/{num_episodes}, Epsilon: {agent.epsilon:.4f}, Avg Reward: {avg_reward:.2f}")
        
        print(f"RL Agent Win Rate: {rl_wins / num_episodes * 100:.2f}%")

        agent.save_q_table("othello_q_table.pickle")
        return agent

if __name__ == "__main__":
    agent = OthelloQLearningAgent.train_rl_agent(num_episodes=100000, gamma=0.9, epsilon=1, decay_rate=0.99996)