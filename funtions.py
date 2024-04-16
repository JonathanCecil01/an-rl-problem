import pygame
ROBOT_SPEED = 5

def simulate_action(actions, robot1, robot2, rod):
    dx1, dy1 = 0, 0
    dx2, dy2 = 0, 0

    if actions[0] == 0:
        rod.moving_robot = robot1
        dx1 = -ROBOT_SPEED
    if actions[0] == 1:
        rod.moving_robot = robot1
        dx1 = ROBOT_SPEED
    if actions[0] == 2:
        rod.moving_robot = robot1
        dy1 = -ROBOT_SPEED
    if actions[0] == 3:
        rod.moving_robot = robot1
        dy1 = ROBOT_SPEED

    if actions[1] == 0:
        rod.moving_robot = robot2
        dx2 = -ROBOT_SPEED
    if actions[1] == 1:
        rod.moving_robot = robot2
        dx2 = ROBOT_SPEED
    if actions[1] == 2:
        rod.moving_robot = robot2
        dy2 = -ROBOT_SPEED
    if actions[1] == 3:
        rod.moving_robot = robot2
        dy2 = ROBOT_SPEED

    return [dx1, dy1, dx2, dy2, rod]
