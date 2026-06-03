from settings import *
from game_object.snake import *
from game_object.fruit import *
from snake_game import Game, screen
from train import Agent, DQN
import torch

# Button layout on the right UI panel
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 40
BUTTON_MARGIN = 20
BUTTON_X = WINDOW_WIDTH + 20
PLUS_BUTTON_Y = 260
MINUS_BUTTON_Y = 260
RESET_BUTTON_Y = 330
START_BUTTON_Y = 400
STOP_BUTTON_Y = 400

OPPOSITE = {
    Direction.UP: Direction.DOWN,
    Direction.DOWN: Direction.UP,
    Direction.LEFT: Direction.RIGHT,
    Direction.RIGHT: Direction.LEFT,
}

def draw_button(rect, text, font, active=True):
    button_color = (60, 60, 60) if active else (0, 0, 0)
    border_color = (255, 255, 255) if active else (100, 100, 100)
    pygame.draw.rect(screen, button_color, rect, border_radius=10)
    pygame.draw.rect(screen, border_color, rect, 2, border_radius=10)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def draw_manual_button(rect, text, font, active=True):
    button_color = (100, 0, 0) if active else (0, 0, 0)
    border_color = (255, 0, 0) if active else (100, 0, 0)
    pygame.draw.rect(screen, button_color, rect, border_radius=10)
    pygame.draw.rect(screen, border_color, rect, 2, border_radius=10)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def draw_speed_panel(speed, font):
    # Draw right panel background
    pygame.draw.rect(screen, (10,10,10), pygame.Rect(WINDOW_WIDTH, 0, SCREEN_WIDTH - WINDOW_WIDTH, SCREEN_HEIGHT))

    title = font.render('Controls', True, (255, 255, 255))
    screen.blit(title, (WINDOW_WIDTH + 20, 20))

    speed_text = font.render(f'Speed: {speed}', True, (255,255,255))
    screen.blit(speed_text, (WINDOW_WIDTH + 20, 60))

    # Speed info
    info_lines = [
        'Click buttons to adjust',
        'game tick speed.',
    ]
    for i, line in enumerate(info_lines):
        line_surf = font.render(line, True, (180, 180, 180))
        screen.blit(line_surf, (WINDOW_WIDTH + 20, 100 + i * 24))

    # Manual control info
    manual_label = font.render('Manual: Arrow keys (or WASD)', True, (200, 200, 200))
    bonus_label = font.render('You can toggle manual control by pressing SPACE too', True, (180, 180, 180))
    screen.blit(manual_label, (WINDOW_WIDTH + 20, 180))
    screen.blit(bonus_label, (WINDOW_WIDTH + 20, 210))

    # Game records summary
    games = globals().get('games_played', 0)
    total = globals().get('total_score', 0)
    avg = (total / games) if games > 0 else 0.0
    records = globals().get('game_records', [])

    stats_x = WINDOW_WIDTH + 20
    stats_y = 520
    games_text = font.render(f'Games: {games}', True, (220, 220, 220))
    avg_text = font.render(f'Average: {avg:.2f}', True, (220, 220, 220))
    best_text = font.render(f'Best: {max(records) if records else 0}', True, (220, 220, 220))

    screen.blit(games_text, (stats_x, stats_y))
    screen.blit(avg_text, (stats_x, stats_y + 22))
    screen.blit(best_text, (stats_x, stats_y + 44))

    recent = font.render('Recent:', True, (200, 200, 200))
    screen.blit(recent, (stats_x, stats_y + 74))
    for i, s in enumerate(records[:6]):
        rtext = font.render(f'{i+1}. {s}', True, (180, 180, 180))
        screen.blit(rtext, (stats_x + 6, stats_y + 100 + i * 20))

    draw_button(minus_button, '-', font)
    draw_button(plus_button, '+', font)
    draw_button(reset_button, 'Reset', font)
    draw_button(start_button, 'Start', font, active=not running)
    draw_button(stop_button, 'Stop', font, active=running)
    draw_manual_button(manual_button, 'Manual control', font, active=manual_control)


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
    agent.local_model.load_state_dict(torch.load('model.pth'))
    agent.local_model.eval()

    game = Game()
    clock = pygame.time.Clock()
    pygame.font.init()
    font = pygame.font.Font('texture/arial.ttf', 18)

    total_score = 0
    games_played = 0
    game_records = []
    current_speed = SPEED
    running = True
    manual_control = False
    mouse_was_pressed = False

    minus_button = pygame.Rect(BUTTON_X, MINUS_BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
    plus_button = pygame.Rect(BUTTON_X + BUTTON_WIDTH + BUTTON_MARGIN, PLUS_BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
    reset_button = pygame.Rect(BUTTON_X, RESET_BUTTON_Y, BUTTON_WIDTH * 2 + BUTTON_MARGIN, BUTTON_HEIGHT)
    start_button = pygame.Rect(BUTTON_X, START_BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
    stop_button = pygame.Rect(BUTTON_X + BUTTON_WIDTH + BUTTON_MARGIN, STOP_BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
    manual_button = pygame.Rect(BUTTON_X, START_BUTTON_Y + BUTTON_HEIGHT + BUTTON_MARGIN, BUTTON_WIDTH * 2 + BUTTON_MARGIN, BUTTON_HEIGHT)

    while True:
        # Check for manual control toggle and handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
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

                # Get action from model (no random exploration)
                state = torch.from_numpy(state_old).float().unsqueeze(0)
                with torch.no_grad():
                    action_values = agent.local_model(state)
                action_index = torch.argmax(action_values).item()
                action = agent._index_to_action(action_index)

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
            pygame.display.flip()

        if running and done:
            total_score += score
            games_played += 1
            # record the finished game's score (most recent first)
            game_records.insert(0, score)
            if len(game_records) > 10:
                game_records.pop()
            avg_score = total_score / games_played
            game.reset()

        clock.tick(current_speed)
