import pygame
ROBOT_SPEED = 5

def simulate_action(keys_pressed, robot1, robot2, rod):
    dx1, dy1 = 0, 0
    dx2, dy2 = 0, 0

    if keys_pressed[pygame.K_LEFT]:
        rod.moving_robot = robot1
        dx1 = -ROBOT_SPEED
    if keys_pressed[pygame.K_RIGHT]:
        rod.moving_robot = robot1
        dx1 = ROBOT_SPEED
    if keys_pressed[pygame.K_UP]:
        rod.moving_robot = robot1
        dy1 = -ROBOT_SPEED
    if keys_pressed[pygame.K_DOWN]:
        rod.moving_robot = robot1
        dy1 = ROBOT_SPEED

    if keys_pressed[pygame.K_a]:
        rod.moving_robot = robot2
        dx2 = -ROBOT_SPEED
    if keys_pressed[pygame.K_d]:
        rod.moving_robot = robot2
        dx2 = ROBOT_SPEED
    if keys_pressed[pygame.K_w]:
        rod.moving_robot = robot2
        dy2 = -ROBOT_SPEED
    if keys_pressed[pygame.K_s]:
        rod.moving_robot = robot2
        dy2 = ROBOT_SPEED

    return [dx1, dy1, dx2, dy2, rod]
