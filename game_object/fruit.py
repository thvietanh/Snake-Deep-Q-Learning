from settings import *

class Fruit:
    def __init__(self):
        self.position = None
        self.spawn()

    def spawn(self, snake_body=None):
        x = random.randint(0, WINDOW_WIDTH // BLOCK_SIZE - 1) * BLOCK_SIZE
        y = random.randint(0, WINDOW_HEIGHT // BLOCK_SIZE - 1) * BLOCK_SIZE
        self.position = Point(x, y)

        if snake_body is None:
            return

        while self.position in snake_body:
            x = random.randint(0, WINDOW_WIDTH // BLOCK_SIZE - 1) * BLOCK_SIZE
            y = random.randint(0, WINDOW_HEIGHT // BLOCK_SIZE - 1) * BLOCK_SIZE
            self.position = Point(x, y)
