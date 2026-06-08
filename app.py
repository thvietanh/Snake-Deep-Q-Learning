import os
import sys

from settings import *
from game_object.snake import *
from game_object.fruit import *
from snake_game import Game, screen
from train import Agent, DQN
import torch

# Resolve paths for development and PyInstaller onefile bundles
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

# Button layout on the right UI panel
BUTTON_WIDTH = 50
BUTTON_HEIGHT = 20
BUTTON_MARGIN = 10
BUTTON_X = WINDOW_WIDTH + 260
PLUS_BUTTON_Y = 75
MINUS_BUTTON_Y = 75
RESET_BUTTON_Y = 110
START_BUTTON_Y = 155
STOP_BUTTON_Y = 155

# Set icon
icon = pygame.image.load(resource_path('texture/apple.png'))
pygame.display.set_icon(icon)

OPPOSITE = {
    Direction.UP: Direction.DOWN,
    Direction.DOWN: Direction.UP,
    Direction.LEFT: Direction.RIGHT,
    Direction.RIGHT: Direction.LEFT,
}

def draw_button(rect, text, font, active=True):
    if active:
        button_color = (80, 120, 200)
        border_color = (120, 180, 255)
        text_color = (255, 255, 255)
    else:
        button_color = (40, 40, 50)
        border_color = (80, 80, 90)
        text_color = (150, 150, 160)
    pygame.draw.rect(screen, button_color, rect, border_radius=10)
    pygame.draw.rect(screen, border_color, rect, 2, border_radius=10)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def draw_manual_button(rect, text, font, active=True):
    if active:
        button_color = (180, 60, 60)
        border_color = (255, 100, 100)
        text_color = (255, 255, 255)
    else:
        button_color = (40, 40, 50)
        border_color = (80, 80, 90)
        text_color = (150, 150, 160)
    pygame.draw.rect(screen, button_color, rect, border_radius=10)
    pygame.draw.rect(screen, border_color, rect, 2, border_radius=10)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def draw_speed_panel(speed, font):
    # Draw right panel background gradient effect
    panel_bg = pygame.Rect(WINDOW_WIDTH, 0, SCREEN_WIDTH - WINDOW_WIDTH, SCREEN_HEIGHT)
    pygame.draw.rect(screen, (12, 12, 18), panel_bg)
    pygame.draw.line(screen, (50, 50, 60), (WINDOW_WIDTH, 0), (WINDOW_WIDTH, SCREEN_HEIGHT), 2)

    # Title section with background
    title_rect = pygame.Rect(WINDOW_WIDTH + 10, 10, SCREEN_WIDTH - WINDOW_WIDTH - 20, 35)
    pygame.draw.rect(screen, (30, 45, 70), title_rect, border_radius=8)
    title = font.render('⚙ CONTROLS', True, (150, 200, 255))
    screen.blit(title, (WINDOW_WIDTH + 20, 17))

    # Speed control section
    speed_y = 60
    speed_label = font.render('Game Speed', True, (200, 200, 210))
    screen.blit(speed_label, (WINDOW_WIDTH + 20, speed_y))
    
    speed_val_text = font.render(f'{speed} ticks/sec', True, (100, 220, 180))
    screen.blit(speed_val_text, (WINDOW_WIDTH + 20, speed_y + 28))
    
    # Speed bar visualization
    speed_bar_width = 200
    speed_bar_height = 10
    speed_bar_x = WINDOW_WIDTH + 20
    speed_bar_y = speed_y + 56
    max_speed = 200
    pygame.draw.rect(screen, (40, 40, 50), pygame.Rect(speed_bar_x, speed_bar_y, speed_bar_width, speed_bar_height))
    filled_width = int((speed / max_speed) * speed_bar_width)
    pygame.draw.rect(screen, (100, 180, 255), pygame.Rect(speed_bar_x, speed_bar_y, filled_width, speed_bar_height))
    pygame.draw.rect(screen, (80, 100, 150), pygame.Rect(speed_bar_x, speed_bar_y, speed_bar_width, speed_bar_height), 1)

    # Manual control info
    manual_y = 135
    manual_label = font.render('Keyboard Controls', True, (200, 200, 210))
    screen.blit(manual_label, (WINDOW_WIDTH + 20, manual_y))
    
    small_font = pygame.font.Font(resource_path('texture/arial.ttf'), 14)
    keys_text = small_font.render('SPACE to toggle manual', True, (180, 180, 190))
    space_text = small_font.render('Arrow keys or WASD to move manually', True, (180, 180, 190))
    screen.blit(keys_text, (WINDOW_WIDTH + 20, manual_y + 26))
    screen.blit(space_text, (WINDOW_WIDTH + 20, manual_y + 42))

    # Game records section with border
    stats_section = pygame.Rect(WINDOW_WIDTH + 10, 225, SCREEN_WIDTH - WINDOW_WIDTH - 20, 190)
    pygame.draw.rect(screen, (25, 35, 50), stats_section, border_radius=8)
    pygame.draw.rect(screen, (60, 80, 120), stats_section, 2, border_radius=8)
    
    games = globals().get('games_played', 0)
    total = globals().get('total_score', 0)
    avg = (total / games) if games > 0 else 0.0
    records = globals().get('game_records', [])

    stats_x = WINDOW_WIDTH + 25
    stats_y = 235
    
    stats_title = font.render('Session Stats', True, (150, 200, 150))
    screen.blit(stats_title, (stats_x, stats_y))
    
    games_text = font.render(f'Games: {games}', True, (220, 220, 220))
    avg_text = font.render(f'Average: {avg:.1f}', True, (220, 220, 220))
    best_text = font.render(f'Best: {best_score}', True, (150, 220, 150))
    
    screen.blit(games_text, (stats_x, stats_y + 32))
    screen.blit(avg_text, (stats_x, stats_y + 56))
    screen.blit(best_text, (stats_x, stats_y + 80))

    recent_label = small_font.render('Recent scores:', True, (160, 160, 170))
    screen.blit(recent_label, (stats_x, stats_y + 110))
    for i, s in enumerate(records[:3]):
        rtext = small_font.render(f'{i+1}. {s}', True, (180, 200, 180))
        screen.blit(rtext, (stats_x + 10, stats_y + 128 + i * 15))

    # Buttons section
    draw_button(minus_button, '-', font)
    draw_button(plus_button, '+', font)
    draw_button(reset_button, 'Reset', font)
    draw_button(start_button, 'Start', font, active=not running)
    draw_button(stop_button, 'Stop', font, active=running)
    draw_manual_button(manual_button, 'Manual', font, active=manual_control)


def draw_network_state(surface, font, input_state, output_values):
    if input_state is None or output_values is None:
        return

    small_font = pygame.font.Font(resource_path('texture/arial.ttf'), 14)
    panel_x = WINDOW_WIDTH + 10
    panel_y = 430
    panel_w = SCREEN_WIDTH - WINDOW_WIDTH - 20
    panel_h = 360
    panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)
    pygame.draw.rect(surface, (20, 25, 40), panel_rect, border_radius=8)
    pygame.draw.rect(surface, (100, 140, 200), panel_rect, 2, border_radius=8)

    title = font.render('Neural Network State', True, (120, 180, 255))
    surface.blit(title, (panel_x + 12, panel_y + 10))
    
    pygame.draw.line(surface, (80, 120, 180), (panel_x + 12, panel_y + 35), (panel_x + panel_w - 12, panel_y + 35), 1)

    # Input nodes section
    input_title = small_font.render('Input Sensors (17)', True, (150, 200, 150))
    surface.blit(input_title, (panel_x + 12, panel_y + 45))
    
    input_x = panel_x + 12
    input_y = panel_y + 65
    line_height = 18
    column_width = panel_w // 2 - 10

    for idx, value in enumerate(input_state.tolist()):
        col = 0 if idx < 9 else 1
        row = idx if idx < 9 else idx - 9
        
        # Create value bar
        bar_width = 80
        bar_height = 6
        bar_x = input_x + col * column_width + 45
        bar_y = input_y + row * line_height + 6
        
        # Normalize value for bar (assuming 0-1 range for most inputs)
        norm_val = max(0, min(1, abs(value)))
        pygame.draw.rect(surface, (40, 50, 70), pygame.Rect(bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(surface, (100, 200, 255), pygame.Rect(bar_x, bar_y, int(bar_width * norm_val), bar_height))
        
        label = f'I{idx + 1}'
        text = small_font.render(label, True, (200, 200, 210))
        surface.blit(text, (input_x + col * column_width, input_y + row * line_height))

    # Output nodes section
    output_x = panel_x + 12
    output_y = panel_y + 220
    output_title = small_font.render('Output Actions (3)', True, (255, 180, 150))
    surface.blit(output_title, (output_x, output_y))
    
    output_y += 25
    best_idx = int(torch.argmax(torch.tensor(output_values)).item())
    action_names = ['Go Straight', 'Turn Left', 'Turn Right']
    
    for idx, value in enumerate(output_values):
        is_selected = idx == best_idx
        
        # Output bar
        bar_width = 120
        bar_height = 14
        bar_x = output_x + 90
        bar_y = output_y + idx * 22
        
        norm_val = max(0, min(1, value))
        bg_color = (60, 30, 30) if is_selected else (0, 0, 0)
        bar_color = (255, 120, 100) if is_selected else (0, 0, 0)
        border_color = (255, 150, 100) if is_selected else (0, 0, 0)
        
        pygame.draw.rect(surface, bg_color, pygame.Rect(bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(surface, bar_color, pygame.Rect(bar_x, bar_y, int(bar_width * norm_val), bar_height))
        pygame.draw.rect(surface, border_color, pygame.Rect(bar_x, bar_y, bar_width, bar_height), 2 if is_selected else 1)
        
        label = small_font.render(action_names[idx], True, (255, 150, 100) if is_selected else (180, 180, 190))
        value_text = small_font.render(f'{value:.2f}', True, (200, 200, 210))
        surface.blit(label, (output_x, output_y + idx * 22 + 2))
        surface.blit(value_text, (output_x + 235, output_y + idx * 22 + 2))


def update_controls_by_click(pos, current_speed, running, manual):
    if minus_button.collidepoint(pos):
        return max(10, current_speed - 10), running, manual
    if plus_button.collidepoint(pos):
        return min(200, current_speed + 10), running, manual
    if reset_button.collidepoint(pos):
        return SPEED, running, manual
    if start_button.collidepoint(pos):
        return current_speed, True, manual
    if stop_button.collidepoint(pos):
        return current_speed, False, manual
    if manual_button.collidepoint(pos):
        return current_speed, running, not manual
    return current_speed, running, manual


if __name__ == '__main__':
    agent = Agent()
    checkpoint = torch.load(resource_path('model.pth'), weights_only=False)
    agent.local_model.load_state_dict(checkpoint['local_model'])
    agent.local_model.eval()

    game = Game()
    clock = pygame.time.Clock()
    pygame.font.init()
    font = pygame.font.Font(resource_path('texture/arial.ttf'), 16)
    
    best_score = 0
    total_score = 0
    games_played = 0
    game_records = []
    current_speed = SPEED
    running = True
    manual_control = False
    mouse_was_pressed = False
    network_state = None
    network_output = None

    minus_button = pygame.Rect(BUTTON_X, MINUS_BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
    plus_button = pygame.Rect(BUTTON_X + BUTTON_WIDTH + BUTTON_MARGIN, PLUS_BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
    reset_button = pygame.Rect(BUTTON_X, RESET_BUTTON_Y, BUTTON_WIDTH * 2 + BUTTON_MARGIN, BUTTON_HEIGHT)
    start_button = pygame.Rect(BUTTON_X, START_BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
    stop_button = pygame.Rect(BUTTON_X + BUTTON_WIDTH + BUTTON_MARGIN, STOP_BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
    manual_button = pygame.Rect(BUTTON_X, 185, BUTTON_WIDTH * 2 + BUTTON_MARGIN, BUTTON_HEIGHT)

    while True:
        # Check for manual control toggle and handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    manual_control = not manual_control
        if running:
            # If manual control is enabled, read keyboard and set snake direction
            if manual_control:
                keys = pygame.key.get_pressed()
                desired = None
                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    desired = Direction.UP
                elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    desired = Direction.DOWN
                elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    desired = Direction.LEFT
                elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    desired = Direction.RIGHT

                if desired is not None and desired != OPPOSITE.get(game.snake.direction):
                    game.snake.direction = desired

                action = [1, 0, 0]
                reward, done, score = game.play_step(action)
            else:
                state_old = agent.get_state(game)
                network_state = state_old

                # Get action from model (no random exploration)
                state = torch.from_numpy(state_old).float().unsqueeze(0)
                with torch.no_grad():
                    action_values = agent.local_model(state)
                action_index = torch.argmax(action_values).item()
                action = agent._index_to_action(action_index)
                network_output = action_values.squeeze(0).cpu().tolist()

                # Perform the action
                reward, done, score = game.play_step(action)
        else:
            game.update()
            done = False
            score = 0

        # Draw speed controls on the right panel
        draw_speed_panel(current_speed, font)

        # Detect button clicks without consuming pygame events twice
        mouse_pressed = pygame.mouse.get_pressed()[0]
        if mouse_pressed and not mouse_was_pressed:
            mouse_pos = pygame.mouse.get_pos()
            current_speed, running, manual_control = update_controls_by_click(mouse_pos, current_speed, running, manual_control)
        mouse_was_pressed = mouse_pressed

        surface = pygame.display.get_surface()
        if surface is not None:
            draw_network_state(surface, font, network_state, network_output)
            pygame.display.flip()

        if running and done:
            total_score += score
            best_score = max(best_score, score)
            games_played += 1
            # record the finished game's score (most recent first)
            game_records.insert(0, score)
            if len(game_records) > 10:
                game_records.pop()
            avg_score = total_score / games_played
            game.reset()

        clock.tick(current_speed)
