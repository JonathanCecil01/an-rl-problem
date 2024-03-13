import pygame
import math


pygame.init()


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Synchronized Robot Movement")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


ROBOT_RADIUS = 30
ROBOT_SPEED = 5


ROD_LENGTH = 100

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


        if distance != 0:
            direction_x = dx / distance
            direction_y = dy / distance


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



robot1 = Robot(200, 300, RED)
robot2 = Robot(600, 300, GREEN)

rod = Rod(robot1, robot2)


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


    robot1.draw()
    robot2.draw()
    rod.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
