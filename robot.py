import pygame
from constants import screen
from constants import ROBOT_RADIUS
#from dqn import *

class Robot:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.angle = 0  # Angle in radians
        #self.reply_memory = ReplayMemory(10000)
        #self.nn = DQN(6, 4)

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), ROBOT_RADIUS)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy


