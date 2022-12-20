import sys, time, random
import snake_game
import pygame
import numpy as np

import math

# This Class defines a Gym Environment my Snake Game
# I want to try different ways of observation_states and reward functions

# The Snake Input is always the same:
# 1. The Frame Size (Game Size) (X,Y)
# 2. The Snake Head Position (X,Y)
# 3. The Snake Tail Positions [(X,Y),..., (X,Y)]
# 4. The Food Position (X,Y)
# 5. The Direction the Snake is facing (up, down, left, right)

# the get_obs function returns a list of 7 values:
# 

class dq_agent_interpreter():

    metadata = {'render.modes': ['human']}

    def __init__(self, sleep=0):
        self.env = snake_game.snake_env(sleep=sleep)
        self.sleep = sleep
        self.env.reset()

        if self.sleep > 0:
            pygame.init()
            frame_size, snake_head, snake_tail, food, _ = self.env.get_state()
            self.screen = pygame.display.set_mode((frame_size[0]*50, frame_size[1]*50))
            self.screen.fill((0,0,0))
        

    def get_state(self):  
        frame_size, snake_head, snake_tail, food, direction = self.env.get_state()
        collisionfront = 0
        collisionleft = 0
        collisionright = 0
        if direction == 'right':
            if snake_head[0] + 1 > frame_size[0]-1 or (snake_head[0] + 1, snake_head[1]) in snake_tail:
                collisionfront = 1
            if snake_head[1] - 1 < 0 or (snake_head[0], snake_head[1] - 1) in snake_tail:
                collisionleft = 1
            if snake_head[1] + 1 > frame_size[1]-1 or (snake_head[0], snake_head[1] + 1) in snake_tail:
                collisionright = 1
        elif direction == 'left':
            if snake_head[0] - 1 < 0 or (snake_head[0] - 1, snake_head[1]) in snake_tail:
                collisionfront = 1
            if snake_head[1] + 1 > frame_size[1]-1 or (snake_head[0], snake_head[1] + 1) in snake_tail:
                collisionleft = 1
            if snake_head[1] - 1 < 0 or (snake_head[0], snake_head[1] - 1) in snake_tail:
                collisionright = 1
        elif direction == 'up':
            if snake_head[1] - 1 < 0 or (snake_head[0], snake_head[1] - 1) in snake_tail:
                collisionfront = 1
            if snake_head[0] - 1 < 0 or (snake_head[0] - 1, snake_head[1]) in snake_tail:
                collisionleft = 1
            if snake_head[0] + 1 > frame_size[0]-1 or (snake_head[0] + 1, snake_head[1]) in snake_tail:
                collisionright = 1
        elif direction == 'down':
            if snake_head[1] + 1 > frame_size[1]-1 or (snake_head[0], snake_head[1] + 1) in snake_tail:
                collisionfront = 1
            if snake_head[0] + 1 > frame_size[0]-1 or (snake_head[0] + 1, snake_head[1]) in snake_tail:
                collisionleft = 1
            if snake_head[0] - 1 < 0 or (snake_head[0] - 1, snake_head[1]) in snake_tail:
                collisionright = 1

        dir_l = direction == 'left'
        dir_r = direction == 'right'
        dir_u = direction == 'up'
        dir_d = direction == 'down'

        state = [
            # Danger Straight
            collisionfront,

            # Danger right
            collisionright,

            #Danger Left
            collisionleft,

            # Move Direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,

            #Food Location
            food[0] < snake_head[0], # food is in left
            food[0] > snake_head[0], # food is in right
            food[1] < snake_head[1], # food is up
            food[1] > snake_head[1]  # food is down
        ]
        return np.array(state,dtype=int)

    def calc_reward(self, pre_state, found_food, game_over):
        _,pre_snake_head,_,_,_ = pre_state
        frame_size, snake_head, snake_tail, food, direction = self.env.get_state()
        reward = 0
        pre_dist = math.sqrt((pre_snake_head[0] - food[0])**2 + (pre_snake_head[1] - food[1])**2)
        dist = math.sqrt((snake_head[0] - food[0])**2 + (snake_head[1] - food[1])**2)
        if dist < pre_dist:
            reward = 1
        elif dist > pre_dist:
            reward = -1

        if found_food:
            reward = 15
        elif game_over:
            reward = -15
        return reward

    def step(self, action): # returns obs, reward, done/over, info
        action = action.index(max(action))
        pre_state = self.env.get_state()
        found_food, game_over, game_done, score, move_count = self.env.play_step(action)
        reward = self.calc_reward(pre_state, found_food, game_over)
        time.sleep(self.sleep)
        return reward, game_done or game_over, score

    def reset(self): #returns observations (obs)
        self.env.reset()
        
    
    def render_state(self, state):    
        frame_size, snake_head, snake_tail, food, _ = state
        if self.sleep > 0:
            self.screen.fill((0,0,0))
            for y in range(frame_size[1]):
                for x in range(frame_size[0]):
                    if (x,y) == snake_head:
                        pygame.draw.rect(self.screen, (255,0,0), (x*50,y*50,50,50))
                    elif (x,y) in snake_tail:
                        pygame.draw.rect(self.screen, (0,255,0), (x*50,y*50,50,50))
                    elif (x,y) == food:
                        pygame.draw.rect(self.screen, (0,0,255), (x*50,y*50,50,50))
                    else:
                        pygame.draw.rect(self.screen, (255,255,255), (x*50,y*50,50,50), 1)
            pygame.display.update()
    
    def render(self):      
        frame_size, snake_head, snake_tail, food, _ = self.env.get_state()             
        if self.sleep > 0:
            self.screen.fill((0,0,0))
            for y in range(frame_size[1]):
                for x in range(frame_size[0]):
                    if (x,y) == snake_head:
                        pygame.draw.rect(self.screen, (255,0,0), (x*50,y*50,50,50))
                    elif (x,y) in snake_tail:
                        pygame.draw.rect(self.screen, (0,255,0), (x*50,y*50,50,50))
                    elif (x,y) == food:
                        pygame.draw.rect(self.screen, (0,0,255), (x*50,y*50,50,50))
                    else:
                        pygame.draw.rect(self.screen, (255,255,255), (x*50,y*50,50,50), 1)
            pygame.display.update()

    def close(self):
        pass



def main():
    ## Observation testing
    env = dq_agent_interpreter()
    env.reset()
    reward = 0
    game_over = False
    env.render()
    while not game_over:    
        action = random.choice([0,1,2])
        observation, step_reward, game_over, info = env.step(action)
        env.render()
        reward += step_reward
        print(observation,"\n")
        print('Action: {}, Reward: {}, Game Over: {}, Info: {}'.format(action, reward, game_over, info))
        
    env.close()
#main()

