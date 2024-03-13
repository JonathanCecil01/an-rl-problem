import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Synchronized Robot Movement")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Robot parameters
ROBOT_RADIUS = 30
ROBOT_SPEED = 5

# Rod parameters
ROD_LENGTH = 100
ROD_THICKNESS = 5

# Wall parameters
WALL_WIDTH = 20

class Robot:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.angle = 0  # Angle in radians

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), ROBOT_RADIUS)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

class Rod:
    def __init__(self, robot1, robot2):
        self.robot1 = robot1
        self.robot2 = robot2
        self.moving_robot = robot1

    def draw(self):
        pygame.draw.line(screen, BLACK, (self.robot1.x, self.robot1.y), (self.robot2.x, self.robot2.y), 5)

    def synchronize(self):
        dx = self.robot2.x - self.robot1.x
        dy = self.robot2.y - self.robot1.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # Normalize the direction vector
        if distance != 0:
            direction_x = dx / distance
            direction_y = dy / distance

            # Calculate the adjustments for each robot based on the desired rod length
            adjustment_x = direction_x * ROD_LENGTH
            adjustment_y = direction_y * ROD_LENGTH

            # Determine which robot's movement to sync based on the direction of movement
            if self.moving_robot == self.robot1:
                new_robot2_x = self.robot1.x + adjustment_x
                new_robot2_y = self.robot1.y + adjustment_y
                self.robot2.x, self.robot2.y = new_robot2_x, new_robot2_y
            elif self.moving_robot == self.robot2:
                new_robot1_x = self.robot2.x - adjustment_x
                new_robot1_y = self.robot2.y - adjustment_y
                self.robot1.x, self.robot1.y = new_robot1_x, new_robot1_y

class Wall:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self):
        pygame.draw.rect(screen, BLUE, self.rect)

# Create walls
wall1 = Wall(100, 100, 20, 400)
wall2 = Wall(100, 100, 600, 20)
wall3 = Wall(100, 480, 600, 20)
wall4 = Wall(680, 100, 20, 400)

# Initialize robots
robot1 = Robot(200, 300, RED)
robot2 = Robot(600, 300, GREEN)

# Initialize rod
rod = Rod(robot1, robot2)

# Main loop
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    dx1, dy1 = 0, 0
    dx2, dy2 = 0, 0
    if keys[pygame.K_LEFT]:
        rod.moving_robot = robot1
        dx1 = -ROBOT_SPEED
    if keys[pygame.K_RIGHT]:
        rod.moving_robot = robot1
        dx1 = ROBOT_SPEED
    if keys[pygame.K_UP]:
        rod.moving_robot = robot1
        dy1 = -ROBOT_SPEED
    if keys[pygame.K_DOWN]:
        rod.moving_robot = robot1
        dy1 = ROBOT_SPEED

    if keys[pygame.K_a]:
        rod.moving_robot = robot2
        dx2 = -ROBOT_SPEED
    if keys[pygame.K_d]:
        rod.moving_robot = robot2
        dx2 = ROBOT_SPEED
    if keys[pygame.K_w]:
        rod.moving_robot = robot2
        dy2 = -ROBOT_SPEED
    if keys[pygame.K_s]:
        rod.moving_robot = robot2
        dy2 = ROBOT_SPEED

    # Move the robots
    robot1.move(dx1, dy1)
    robot2.move(dx2, dy2)


    # Synchronize movement of rod with robots
    rod.synchronize()

    # Draw everything
    robot1.draw()
    robot2.draw()
    rod.draw()
    wall1.draw()
    wall2.draw()
    wall3.draw()
    wall4.draw()

    # Define door dimensions and position
    door_width = 100
    door_height = 20
    door_x = (WIDTH - door_width) // 2  # Center the door horizontally
    door_y = HEIGHT - 120 # Place the door at the bottom wall

    # Create the door rectangle
    bottom_wall_opening = pygame.Rect(door_x, door_y, door_width, door_height)

    # Draw the door in the bottom wall
    pygame.draw.rect(screen, BLACK, bottom_wall_opening)

    # Collision detection with walls for the rod
    rod_rect = pygame.Rect(min(robot1.x, robot2.x), min(robot1.y, robot2.y),
                           abs(robot2.x - robot1.x), abs(robot2.y - robot1.y))
    rod_rect.inflate_ip(ROD_LENGTH // 2, ROD_LENGTH // 2)  # Inflate the rectangle vertically by half the thickness

    # Exclude the door area from collision detection
    door_rect = pygame.Rect(door_x, door_y, door_width, door_height)

    # Perform collision detection with walls, excluding the door area
    for wall in [wall1, wall2, wall3, wall4]:
        if wall.rect.colliderect(rod_rect) and not door_rect.colliderect(rod_rect):
            # If there's a collision with any wall but not the door, adjust both robots' positions
            robot1.x -= dx1
            robot1.y -= dy1
            robot2.x -= dx2
            robot2.y -= dy2

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
