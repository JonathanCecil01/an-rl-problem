import pygame
import math
from constants import  BLACK
from constants import  ROD_LENGTH , ROD_THICKNESS
from constants import  screen
from constants import WIDTH, HEIGHT

class Rod:
    def __init__(self, robot1, robot2):
        self.robot1 = robot1
        self.robot2 = robot2
        self.moving_robot = robot1

    def draw(self):
        pygame.draw.line(screen, BLACK, (self.robot1.x, self.robot1.y), (self.robot2.x, self.robot2.y), ROD_THICKNESS)

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

    def is_outside_room(self):
        rod_center_x = (self.robot1.x + self.robot2.x) / 2
        rod_center_y = (self.robot1.y + self.robot2.y) / 2

        # Check if the rod's center lies outside the room boundaries
        if (rod_center_x < 0 or rod_center_x > WIDTH or
                rod_center_y < 0 or rod_center_y > HEIGHT):
            return True  # Rod is outside the room
        else:
            return False  # Rod is inside the room