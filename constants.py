
import  pygame


# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Robot parameters
ROBOT_RADIUS = 20
ROBOT_SPEED = 5

# Rod parameters
ROD_LENGTH = 100
ROD_THICKNESS = 10

# Wall parameters
WALL_WIDTH = 20