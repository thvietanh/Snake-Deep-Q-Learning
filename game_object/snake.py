from settings import *

class Snake:
    def __init__(self):
        # Snake starts with 3 blocks in the middle of the screen, moving to the right
        self.body = [Point(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), Point(WINDOW_WIDTH // 2 - BLOCK_SIZE, WINDOW_HEIGHT // 2), Point(WINDOW_WIDTH // 2 - 2 * BLOCK_SIZE, WINDOW_HEIGHT // 2)]
        self.direction = Direction.RIGHT
    
    def change_direction(self, action):
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_direction = self.direction
        elif np.array_equal(action, [0, 1, 0]):
            new_direction = clock_wise[(idx + 1) % 4]
        elif np.array_equal(action, [0, 0, 1]):
            new_direction = clock_wise[(idx - 1) % 4]
        else:
            new_direction = self.direction

        self.direction = new_direction
    
    def move(self):
        head = self.body[0]
        if self.direction == Direction.RIGHT:
            new_head = Point(head.x + BLOCK_SIZE, head.y)
        elif self.direction == Direction.LEFT:
            new_head = Point(head.x - BLOCK_SIZE, head.y)
        elif self.direction == Direction.UP:
            new_head = Point(head.x, head.y - BLOCK_SIZE)
        elif self.direction == Direction.DOWN:
            new_head = Point(head.x, head.y + BLOCK_SIZE)
        
        self.body.insert(0, new_head)

    def check_collision(self, point=None):
        if point is None:
            point = self.body[0]

        if point.x < 0 or point.x >= WINDOW_WIDTH or point.y < 0 or point.y >= WINDOW_HEIGHT:
            return True
        if point in self.body[1:]:
            return True
        return False