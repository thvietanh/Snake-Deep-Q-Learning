from settings import *
from game_object.snake import *
from game_object.fruit import *
from snake_game import Game
from train import Agent, DQN
import torch

if __name__ == '__main__':
    agent = Agent()
    agent.local_model.load_state_dict(torch.load('model.pth'))
    agent.local_model.eval()
    
    game = Game()
    clock = pygame.time.Clock()
    total_score = 0
    games_played = 0

    print("Playing...")
    
    while True:
        state_old = agent.get_state(game)
        
        # Get action from model (no random exploration)
        state = torch.from_numpy(state_old).float().unsqueeze(0)
        with torch.no_grad():
            action_values = agent.local_model(state)
        action_index = torch.argmax(action_values).item()
        action = agent._index_to_action(action_index)
        
        # Perform the action
        reward, done, score = game.play_step(action)
        
        # Update display
        surface = pygame.display.get_surface()
        if surface is not None:
            pygame.display.flip()
        
        if done:
            total_score += score
            games_played += 1
            avg_score = total_score / games_played
            print(f"Game {games_played} Over! Score: {score} | Average: {avg_score:.2f}")
            game.reset()
        
        clock.tick(SPEED)
