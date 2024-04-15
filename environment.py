from constants import ROBOT_SPEED
from wall import  Wall
import pygame
from constants import HEIGHT , WIDTH, ROD_LENGTH
import torch


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#defining the wall
wall1 = Wall(100, 100, 20, 400)
wall2 = Wall(100, 100, 600, 20)
wall3 = Wall(100, 480, 600, 20)
wall4 = Wall(680, 100, 20, 400)

# Define door dimensions and position
door_width = 100
door_height = 20
door_x = (WIDTH - door_width) // 2  # Center the door horizontally
door_y = HEIGHT - 120  # Place the door at the bottom wall

# Create the door rectangle
bottom_wall_opening = pygame.Rect(door_x, door_y, door_width, door_height)




class Environment:
    def __init__(self, robot1, rod , robot2):

        self.rod = rod
        self.robot1 = robot1
        self.robot2 = robot2
        self.rod_x = None
        self.rod_y = None
        self.actions = [0, 1, 2, 3]
        self.possible_agents = ['robot1', 'robot2']

    #returns a random start state for the robot
    def reset(self):
        self.robot1.x = 200
        self.robot1.y = 300
        self.robot2.x = 600
        self.robot2.y = 300

        self.rod_x = (self.robot1.x + self.robot2.x) / 2
        self.rod_y = (self.robot1.y + self.robot2.y) / 2

        observations = {
            a:((self.robot1.x , self.robot2.y) , ROBOT_SPEED ,
               (self.rod_x ,self.rod_y ) , ROBOT_SPEED ,
               (self.robot2.x , self.robot2.y) , ROBOT_SPEED) for a in self.possible_agents
        }

        return observations
    

    #returns the list of all possible actions
    def action_space(self):
        return self.actions

    def get_reward(self, state):
        return 1

    #returns the next step, reward, if End state flag 
    def step(self,action,agent):
        dx1, dy1 = 0, 0
        dx2, dy2 = 0, 0

        if agent == 'robot1':
            if action == 0:#'left':
                self.robot1.x = self.robot1.x - ROBOT_SPEED
                dx1 = -ROBOT_SPEED
            if action == 1:#'right':
                self.robot1.x  =  self.robot1.x + ROBOT_SPEED
                dx1 = ROBOT_SPEED
            if action == 2:#'up':
                self.robot1.y = self.robot1.y -ROBOT_SPEED
                dy1 = -ROBOT_SPEED
            if action == 3:#'down':
                self.robot1.y = self.robot1.y + ROBOT_SPEED
                dy1 = ROBOT_SPEED
        if agent == 'robot2':
            if action == 'left':
                self.robot2.x = self.robot2.x - ROBOT_SPEED
                dx2 = -ROBOT_SPEED
            if action == 'right':
                self.robot2.x  =  self.robot2.x + ROBOT_SPEED
                dx2 = ROBOT_SPEED
            if action == 'up':
                self.robot2.y = self.robot2.y -ROBOT_SPEED
                dy2 = -ROBOT_SPEED
            if action == 'down':
                self.robot2.y = self.robot2.y + ROBOT_SPEED
                dy2 = ROBOT_SPEED

        self.rod_x = (self.robot1.x + self.robot2.x) / 2
        self.rod_y =(self.robot1.y + self.robot2.y) / 2
        next_state = [(self.robot1.x , self.robot1.y),ROBOT_SPEED ,(self.rod_x , self.rod_y) , ROBOT_SPEED , (self.robot2.x , self.robot2.y ), ROBOT_SPEED]
        next_state = [next_state[0][0], next_state[0][1], next_state[1], next_state[2][0], next_state[2][1], next_state[3], next_state[4][0], next_state[4][1]]
        next_state = torch.tensor(next_state, dtype=torch.float32, device=device).unsqueeze(0)
        reward = self.get_reward(next_state)
        self.rod.synchronize()

        reward = 0
        # Collision detection with walls for the rod
        rod_rect = pygame.Rect(min(self.robot1.x, self.robot2.x), min(self.robot1.y, self.robot2.y),
                               abs(self.robot2.x - self.robot1.x), abs(self.robot2.y - self.robot1.y))
        rod_rect.inflate_ip(ROD_LENGTH // 2, ROD_LENGTH // 2)  # Inflate the rectangle vertically by half the thickness

        # Exclude the door area from collision detection
        door_rect = pygame.Rect(door_x, door_y, door_width, door_height)

        # Perform collision detection with walls, excluding the door area
        for wall in [wall1, wall2, wall3, wall4]:
            if wall.rect.colliderect(rod_rect) and not door_rect.colliderect(rod_rect):
                # If there's a collision with any wall but not the door, adjust both robots' positions
                reward =  -100
                self.robot1.x -= dx1
                self.robot1.y -= dy1
                self.robot2.x -= dx2
                self.robot2.y -= dy2
            else:
                reward =  0.01

        isEnd = self.rod.is_outside_room()
        if isEnd :
            reward =  400


        return next_state, reward, isEnd



