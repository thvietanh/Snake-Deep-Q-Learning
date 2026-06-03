import pygame
import random
import numpy as np
import math
from enum import Enum
from collections import namedtuple
from collections import deque

# Window size
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800

# Screen size
SCREEN_HEIGHT = 800
SCREEN_WIDTH = 1240
# Size of each block in the game
BLOCK_SIZE = 40
# Speed of the game (higher number means faster training but more CPU usage)
SPEED = 30

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]

Point = namedtuple('Point', 'x, y')

#Colors
RED = (200, 0, 0)
GREEN = (166, 208, 87)
GRAY = (100, 100, 100)
BLUE = (73, 117, 230)
ORANGE = (174, 214, 94)

# Get-ChildItem -Path . -Filter __pycache__ -Recurse -Directory | Remove-Item -Recurse -Force