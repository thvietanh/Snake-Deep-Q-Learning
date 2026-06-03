import os
import sys

from settings import *
from game_object.snake import *
from game_object.fruit import *

# Resolve paths for development and PyInstaller onefile bundles
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

# Use hardware surface + double buffering to reduce flicker/tearing
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption('Snake AI Training')

# Load texture
fruit_texture = pygame.image.load(resource_path('texture/apple.png')).convert_alpha()
fruit_texture = pygame.transform.scale(fruit_texture, (BLOCK_SIZE, BLOCK_SIZE))

snake_head_texture = {
    Direction.UP: pygame.transform.scale(pygame.image.load(resource_path('texture/snake/head_up.png')).convert_alpha(), (BLOCK_SIZE, BLOCK_SIZE)),
    Direction.DOWN: pygame.transform.scale(pygame.image.load(resource_path('texture/snake/head_down.png')).convert_alpha(), (BLOCK_SIZE, BLOCK_SIZE)),
    Direction.LEFT: pygame.transform.scale(pygame.image.load(resource_path('texture/snake/head_left.png')).convert_alpha(), (BLOCK_SIZE, BLOCK_SIZE)),
    Direction.RIGHT: pygame.transform.scale(pygame.image.load(resource_path('texture/snake/head_right.png')).convert_alpha(), (BLOCK_SIZE, BLOCK_SIZE)),
}

snake_tail_texture = {
    Direction.UP: pygame.transform.scale(pygame.image.load(resource_path('texture/snake/tail_up.png')).convert_alpha(), (BLOCK_SIZE, BLOCK_SIZE)),
    Direction.DOWN: pygame.transform.scale(pygame.image.load(resource_path('texture/snake/tail_down.png')).convert_alpha(), (BLOCK_SIZE, BLOCK_SIZE)),
    Direction.LEFT: pygame.transform.scale(pygame.image.load(resource_path('texture/snake/tail_left.png')).convert_alpha(), (BLOCK_SIZE, BLOCK_SIZE)),
    Direction.RIGHT: pygame.transform.scale(pygame.image.load(resource_path('texture/snake/tail_right.png')).convert_alpha(), (BLOCK_SIZE, BLOCK_SIZE)),
}

snake_body_texture = {
    'vertical': pygame.transform.scale(pygame.image.load(resource_path('texture/snake/body_vertical.png')).convert_alpha(), (BLOCK_SIZE, BLOCK_SIZE)),
    'horizontal': pygame.transform.scale(pygame.image.load(resource_path('texture/snake/body_horizontal.png')).convert_alpha(), (BLOCK_SIZE, BLOCK_SIZE)),
    'topleft': pygame.transform.scale(pygame.image.load(resource_path('texture/snake/body_topleft.png')).convert_alpha(), (BLOCK_SIZE, BLOCK_SIZE)),
    'topright': pygame.transform.scale(pygame.image.load(resource_path('texture/snake/body_topright.png')).convert_alpha(), (BLOCK_SIZE, BLOCK_SIZE)),
    'bottomleft': pygame.transform.scale(pygame.image.load(resource_path('texture/snake/body_bottomleft.png')).convert_alpha(), (BLOCK_SIZE, BLOCK_SIZE)),
    'bottomright': pygame.transform.scale(pygame.image.load(resource_path('texture/snake/body_bottomright.png')).convert_alpha(), (BLOCK_SIZE, BLOCK_SIZE)),
}


def get_direction(source, target):
    if target.x > source.x:
        return Direction.RIGHT
    if target.x < source.x:
        return Direction.LEFT
    if target.y > source.y:
        return Direction.DOWN
    if target.y < source.y:
        return Direction.UP
    return None


def get_body_texture(prev_point, point, next_point):
    prev_dir = get_direction(point, prev_point)
    next_dir = get_direction(point, next_point)

    directions = {prev_dir, next_dir}
    
    # Check for straight segments
    if directions == {Direction.UP, Direction.DOWN}:
        return snake_body_texture['vertical']
    if directions == {Direction.LEFT, Direction.RIGHT}:
        return snake_body_texture['horizontal']
    
    # Check for corner segments
    if directions == {Direction.UP, Direction.LEFT}:
        return snake_body_texture['topleft']
    if directions == {Direction.UP, Direction.RIGHT}:
        return snake_body_texture['topright']
    if directions == {Direction.DOWN, Direction.LEFT}:
        return snake_body_texture['bottomleft']
    if directions == {Direction.DOWN, Direction.RIGHT}:
        return snake_body_texture['bottomright']

    return snake_body_texture['horizontal']


def get_tail_texture(tail_point, prev_point):
    # Tail texture should point away from the body connection.
    body_dir = get_direction(tail_point, prev_point)
    if body_dir == Direction.LEFT:
        return snake_tail_texture[Direction.RIGHT]
    if body_dir == Direction.RIGHT:
        return snake_tail_texture[Direction.LEFT]
    if body_dir == Direction.UP:
        return snake_tail_texture[Direction.DOWN]
    if body_dir == Direction.DOWN:
        return snake_tail_texture[Direction.UP]
    return snake_tail_texture[Direction.RIGHT]

class Game:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.score = 0
        self.reward = 0
        self.gameOver = False
        self.frame_iteration = 0
        self.animation_tick = 0
        self.fruit.spawn(self.snake.body)

    def reset(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.score = 0
        self.reward = 0
        self.gameOver = False
        self.frame_iteration = 0
        self.fruit.spawn(self.snake.body)
    
    def play_step(self, action):
        self.frame_iteration += 1
        old_head = Point(self.snake.body[0].x, self.snake.body[0].y)
        old_distance = abs(old_head.x - self.fruit.position.x) + abs(old_head.y - self.fruit.position.y)

        self.snake.change_direction(action)
        self.snake.move()

        self.reward = 0
        self.gameOver = False

        if self.snake.check_collision():
            self.gameOver = True
            self.reward = -10
            return self.reward, self.gameOver, self.score

        if self.frame_iteration > 100 * len(self.snake.body):
            self.gameOver = True
            self.reward = -10
            return self.reward, self.gameOver, self.score

        if self.snake.body[0] == self.fruit.position:
            self.score += 1
            self.reward = 10
            eat_center_x = self.fruit.position.x + BLOCK_SIZE // 2
            eat_center_y = self.fruit.position.y + BLOCK_SIZE // 2
            self.fruit.spawn(self.snake.body)
        else:
            self.snake.body.pop()
            new_distance = abs(self.snake.body[0].x - self.fruit.position.x) + abs(self.snake.body[0].y - self.fruit.position.y)
            if new_distance < old_distance:
                self.reward += 0.1
            elif new_distance > old_distance:
                self.reward -= 0.1

        self.update()

        return self.reward, self.gameOver, self.score
    
    def game_over(self):
        self.reward = -10
        self.gameOver = True
        return self.reward, self.gameOver, self.score

    
    def update(self):
        self.animation_tick += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.fill((0, 0, 0))
        # Draw board
        for x in range(0,WINDOW_HEIGHT, BLOCK_SIZE):
            for y in range(0,WINDOW_WIDTH, BLOCK_SIZE):
                if (x+y) % (BLOCK_SIZE * 2) == 0:
                    pygame.draw.rect(screen, GREEN, pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE))
                else:
                    pygame.draw.rect(screen, ORANGE, pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE))

        for idx, point in enumerate(self.snake.body):
            if idx == 0:
                texture = snake_head_texture[self.snake.direction]
            elif idx == len(self.snake.body) - 1:
                prev_point = self.snake.body[idx - 1]
                texture = get_tail_texture(point, prev_point)
            else:
                prev_point = self.snake.body[idx - 1]
                next_point = self.snake.body[idx + 1]
                texture = get_body_texture(prev_point, point, next_point)

            screen.blit(texture, (point.x, point.y))

            # Add a subtle animation effect: pulsing head glow and body shimmer
            if idx == 0:
                glow_alpha = int((math.sin(self.animation_tick * 0.15) + 1) * 50)
                glow_surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                pygame.draw.circle(glow_surface, (255, 255, 255, glow_alpha), (BLOCK_SIZE // 2, BLOCK_SIZE // 2), BLOCK_SIZE // 2)
                screen.blit(glow_surface, (point.x, point.y))
            else:
                shimmer_alpha = int((math.sin(self.animation_tick * 0.12 + idx * 0.5) + 1) * 12)
                if shimmer_alpha > 0:
                    shimmer_surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
                    shimmer_surface.fill((255, 255, 255, shimmer_alpha))
                    screen.blit(shimmer_surface, (point.x, point.y))

        screen.blit(fruit_texture, (self.fruit.position.x, self.fruit.position.y))
        # Separator line moved to match the larger training plot area
        pygame.draw.line(screen, GRAY, (WINDOW_WIDTH, 0), (WINDOW_HEIGHT, SCREEN_HEIGHT))
        # Timing and screen flip are handled in the main loop to avoid double buffering issues
