from settings import *
from game_object.snake import *
from game_object.fruit import *
from snake_game import Game
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os

# Plotting
from plotting import TrainingPlotter
plotter = TrainingPlotter()

# Hyperparameters
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
EPSILON = 100  # Initial exploration 
E_DECAY = 0.001  # Decay rate for exploration
GAMMA = 0.9 # Discount factor for future rewards
LEARNING_RATE = 0.001

class DQN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(DQN, self).__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x
    
class ReplayMemory:
    def __init__(self, capacity):
        self.memory = deque(maxlen=capacity)

    def push(self, experience):
        self.memory.append(experience)
        if len(self.memory) > MAX_MEMORY:
            del self.memory[0]

    def sample(self, k):
        experiences = random.sample(self.memory, k=k)
        states, actions, rewards, next_states, dones = zip(*experiences)
        return states, actions, rewards, next_states, dones

    def __len__(self):
        return len(self.memory)
    
class Agent:
    def __init__(self):
        # Configure the sizes of the state, action, and hidden layers for the DQN
        self.state_size = 11
        self.action_size = 3
        self.hidden_size = 256

        # Set models, optimizer, and replay memory for the DQN agent
        self.local_model = DQN(self.state_size, self.hidden_size, self.action_size)
        self.target_model = DQN(self.state_size, self.hidden_size, self.action_size)
        self.optimizer = optim.Adam(self.local_model.parameters(), lr=LEARNING_RATE)
        self.memory = ReplayMemory(MAX_MEMORY)
        self.number_of_games = 0

        # Hyperparameters for epsilon-greedy action selection
        self.epsilon = EPSILON
        self.gamma = GAMMA
        self.blend_factor = 0.01

    def get_state(self, game):
        head = game.snake.body[0]
        point_l = Point(head.x - BLOCK_SIZE, head.y)
        point_r = Point(head.x + BLOCK_SIZE, head.y)
        point_u = Point(head.x, head.y - BLOCK_SIZE)
        point_d = Point(head.x, head.y + BLOCK_SIZE)

        dir_l = game.snake.direction == Direction.LEFT
        dir_r = game.snake.direction == Direction.RIGHT
        dir_u = game.snake.direction == Direction.UP
        dir_d = game.snake.direction == Direction.DOWN

        state = [
            # Danger straight
            (dir_r and game.snake.check_collision(point_r)) or 
            (dir_l and game.snake.check_collision(point_l)) or 
            (dir_u and game.snake.check_collision(point_u)) or 
            (dir_d and game.snake.check_collision(point_d)),

            # Danger right
            (dir_u and game.snake.check_collision(point_r)) or 
            (dir_d and game.snake.check_collision(point_l)) or 
            (dir_l and game.snake.check_collision(point_u)) or 
            (dir_r and game.snake.check_collision(point_d)),

            # Danger left
            (dir_d and game.snake.check_collision(point_r)) or 
            (dir_u and game.snake.check_collision(point_l)) or 
            (dir_r and game.snake.check_collision(point_u)) or 
            (dir_l and game.snake.check_collision(point_d)),

            dir_l,
            dir_r,
            dir_u,
            dir_d,

            game.fruit.position.x < game.snake.body[0].x,
            game.fruit.position.x > game.snake.body[0].x,
            game.fruit.position.y < game.snake.body[0].y,
            game.fruit.position.y > game.snake.body[0].y
        ]

        return np.array(state, dtype=int)
    
    # Push the experience tuple (state, action, reward, next_state, done) into the replay memory
    def remember(self, state, action, reward, next_state, done):
        self.memory.push((state, action, reward, next_state, done))
 
    # Convert action vector
    def _index_to_action(self, action_index):
        action = [0] * self.action_size
        action[action_index] = 1
        return action
    
    # Get current state of the game and decide on an action using epsilon-greedy strategy
    def get_action(self, state):
        state = torch.from_numpy(state).float().unsqueeze(0)
        self.local_model.eval()
        with torch.no_grad():
            action_values = self.local_model(state)  # Q values for all actions
        self.local_model.train()

        if random.uniform(0.0, 99.0) < self.epsilon:
            move = random.randint(0, self.action_size - 1)
        else:
            move = torch.argmax(action_values).item()

        return move
    
    def learn(self, experiences):
        states, actions, rewards, next_states, dones = experiences

        states = torch.tensor(np.vstack(states), dtype=torch.float32)
        actions = torch.tensor(actions, dtype=torch.long).unsqueeze(1)
        rewards = torch.tensor(rewards, dtype=torch.float32).unsqueeze(1)
        next_states = torch.tensor(np.vstack(next_states), dtype=torch.float32)
        dones = torch.tensor(dones, dtype=torch.float32).unsqueeze(1)

        next_q_values = self.target_model(next_states).detach().max(1)[0].unsqueeze(1)

        target_q_values = rewards + self.gamma * next_q_values * (1 - dones)

        expected_q_values = self.local_model(states).gather(1, actions)

        loss = F.mse_loss(expected_q_values, target_q_values)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        self.soft_update(self.local_model, self.target_model, tau=self.blend_factor)

    def soft_update(self, local_model, target_model, tau):
        # Combine local and target model parameters using a blend factor tau
        for local_param, target_param in zip(local_model.parameters(), target_model.parameters()):
            target_param.data.copy_(tau * local_param.data + (1.0 - tau) * target_param.data)

    # Save model to file
    def save_model(self, file_name='model.pth'):
        torch.save(self.local_model.state_dict(), file_name)

if __name__ == '__main__':
    agent = Agent()
    game = Game()
    clock = pygame.time.Clock()

    while True:
        # Get the current state of the game
        state_old = agent.get_state(game)

        # Get the action index to take based on the current state
        action_index = agent.get_action(state_old)
        action = agent._index_to_action(action_index)

        # Perform the action and get the new state and reward
        reward, done, score = game.play_step(action)
        state_new = agent.get_state(game)

        # Remember the experience for replay memory
        agent.remember(state_old, action_index, reward, state_new, done)

        # Learn from past experiences if there are enough in memory
        if len(agent.memory) > BATCH_SIZE:
            experiences = agent.memory.sample(BATCH_SIZE)
            agent.learn(experiences)

        if done:
            if agent.epsilon > 0:
                agent.epsilon = np.exp(-agent.number_of_games // 2 * E_DECAY) * agent.epsilon  # Decay epsilon after each game to reduce exploration over time
                # Decay epsilon after each game to reduce exploration over time
            plotter.update(score)
            # Reset the game and increment the number of games played
            game.reset()
            agent.number_of_games += 1

            # Save the model every 10 games
            if agent.number_of_games % 10 == 0:
                agent.save_model()

        surface = pygame.display.get_surface()
        if surface is not None:
            plotter.update_epsilon(agent.epsilon)
            plotter.draw(surface)
            pygame.display.flip()
            clock.tick(SPEED)
