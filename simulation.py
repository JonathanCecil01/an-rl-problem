import pygame
import math


from constants import  *
from robot import Robot
from rod import Rod
from wall import Wall
from funtions import simulate_action
# Initialize Pygame
pygame.init()
pygame.display.set_caption("Synchronized Robot Movement")


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
    [dx1, dy1, dx2, dy2, rod] = simulate_action(keys,robot1,robot2 ,rod)

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
