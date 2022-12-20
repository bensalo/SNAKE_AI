import sys, time, random
import gym
import snake_game

import numpy as np
from gym import Env, spaces

import math

# This Class defines a Gym Environment my Snake Game
# I want to try different ways of observation_states and reward functions

# The Snake Input is always the same:
# 1. The Frame Size (Game Size) (X,Y)
# 2. The Snake Head Position (X,Y)
# 3. The Snake Tail Positions [(X,Y),..., (X,Y)]
# 4. The Food Position (X,Y)
# 5. The Direction the Snake is facing (up, down, left, right)

# the get_obs function returns 2 values
# 1. The direction of the food (8 states)
# 2. Collision in front, left, right (8 states)
# 

class snake_agent_env(gym.Env):

    metadata = {'render.modes': ['human']}

    def __init__(self, sleep=0):
        self.env = snake_game.snake_env()
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Discrete(64)
        self.sleep = sleep
        self.env.reset()
        

    def get_obs(self, frame_size, snake_head, snake_tail, food, dir):
        foodq1 = 0
        foodq2 = 0
        foodq3 = 0
        foodq4 = 0
        collisionfront = 0
        collisionleft = 0
        collisionright = 0

        if dir == 'right':
            if food[0] >= snake_head[0] and food[1] <= snake_head[1]:
                foodq1 = 1
            if food[0] <= snake_head[0] and food[1] <= snake_head[1]:
                foodq2 = 1
            if food[0] <= snake_head[0] and food[1] >= snake_head[1]:
                foodq3 = 1
            if food[0] >= snake_head[0] and food[1] >= snake_head[1]:
                foodq4 = 1
            if snake_head[0] + 1 > frame_size[0]-1 or (snake_head[0] + 1, snake_head[1]) in snake_tail:
                collisionfront = 1
            if snake_head[1] - 1 < 0 or (snake_head[0], snake_head[1] - 1) in snake_tail:
                collisionleft = 1
            if snake_head[1] + 1 > frame_size[1]-1 or (snake_head[0], snake_head[1] + 1) in snake_tail:
                collisionright = 1
        elif dir == 'left':
            if food[0] <= snake_head[0] and food[1] >= snake_head[1]:
                foodq1 = 1
            if food[0] >= snake_head[0] and food[1] >= snake_head[1]:
                foodq2 = 1
            if food[0] >= snake_head[0] and food[1] <= snake_head[1]:
                foodq3 = 1
            if food[0] <= snake_head[0] and food[1] <= snake_head[1]:
                foodq4 = 1
            if snake_head[0] - 1 < 0 or (snake_head[0] - 1, snake_head[1]) in snake_tail:
                collisionfront = 1
            if snake_head[1] + 1 > frame_size[1]-1 or (snake_head[0], snake_head[1] + 1) in snake_tail:
                collisionleft = 1
            if snake_head[1] - 1 < 0 or (snake_head[0], snake_head[1] - 1) in snake_tail:
                collisionright = 1
        elif dir == 'up':
            if food[1] <= snake_head[1] and food[0] <= snake_head[0]:
                foodq1 = 1
            if food[1] >= snake_head[1] and food[0] <= snake_head[0]:
                foodq2 = 1
            if food[1] >= snake_head[1] and food[0] >= snake_head[0]:
                foodq3 = 1
            if food[1] <= snake_head[1] and food[0] >= snake_head[0]:
                foodq4 = 1
            if snake_head[1] - 1 < 0 or (snake_head[0], snake_head[1] - 1) in snake_tail:
                collisionfront = 1
            if snake_head[0] - 1 < 0 or (snake_head[0] - 1, snake_head[1]) in snake_tail:
                collisionleft = 1
            if snake_head[0] + 1 > frame_size[0]-1 or (snake_head[0] + 1, snake_head[1]) in snake_tail:
                collisionright = 1
        elif dir == 'down':
            if food[1] >= snake_head[1] and food[0] >= snake_head[0]:
                foodq1 = 1
            if food[1] <= snake_head[1] and food[0] >= snake_head[0]:
                foodq2 = 1
            if food[1] <= snake_head[1] and food[0] <= snake_head[0]:
                foodq3 = 1
            if food[1] >= snake_head[1] and food[0] <= snake_head[0]:
                foodq4 = 1
            if snake_head[1] + 1 > frame_size[1]-1 or (snake_head[0], snake_head[1] + 1) in snake_tail:
                collisionfront = 1
            if snake_head[0] + 1 > frame_size[0]-1 or (snake_head[0] + 1, snake_head[1]) in snake_tail:
                collisionleft = 1
            if snake_head[0] - 1 < 0 or (snake_head[0] - 1, snake_head[1]) in snake_tail:
                collisionright = 1
        
        food_dir = str(foodq1) + str(foodq2) + str(foodq3) + str(foodq4)
        collision_dir = str(collisionfront) + str(collisionleft) + str(collisionright)
        
        if food_dir == '0001':
            ret_dir = 0
        elif food_dir == '0010':
            ret_dir = 1
        elif food_dir == '0100':
            ret_dir = 2
        elif food_dir == '1000':
            ret_dir = 3
        elif food_dir == '0011':
            ret_dir = 4
        elif food_dir == '0110':
            ret_dir = 5
        elif food_dir == '1100':
            ret_dir = 6
        elif food_dir == '1001':
            ret_dir = 7
        
        if collision_dir == '000':
            ret_col = 0
        elif collision_dir == '001':
            ret_col = 1
        elif collision_dir == '010':
            ret_col = 2
        elif collision_dir == '100':
            ret_col = 3
        elif collision_dir == '011':
            ret_col = 4
        elif collision_dir == '101':
            ret_col = 5
        elif collision_dir == '110':
            ret_col = 6
        elif collision_dir == '111':
            ret_col = 7

        # display all possible combinations of ret_dir and ret_col o 0-63

        


        return (ret_dir, ret_col)

    def get_state(self):
        frame_size, snake_head, snake_tail, food, dir = self.env.get_state()
        return self.get_obs(frame_size, snake_head, snake_tail, food, dir)

    def calc_reward(self, pre_state, found_food, game_over, game_done): # rewards function überarbeiten !!!
        reward = 0
        _, pre_snake_head, _, food, _ = pre_state
        _, snake_head, _, food, _ = self.env.get_state()

        if found_food:
            reward += 20
        if game_over:
            reward -= 20
        if game_done:
            reward += 10
        
        pre_x_dist = abs(food[0] - pre_snake_head[0])
        pre_y_dist = abs(food[1] - pre_snake_head[1])
        x_dist = abs(food[0] - snake_head[0])
        y_dist = abs(food[1] - snake_head[1])

        if pre_x_dist > x_dist:
            reward += 5
        else:
            reward -= 3
        
        if pre_y_dist > y_dist:
            reward += 5
        else:
            reward -= 3

        return reward

    def step(self, action): # returns obs, reward, done/over, info
        pre_state = self.env.get_state()
        found_food, game_over, game_done, score, move_count = self.env.play_step(action)
        reward = self.calc_reward(pre_state,found_food, game_over, game_done)
        info = {'score': score, 'move_count': move_count}
        time.sleep(self.sleep)
        return self.get_state(), reward, game_done or game_over, info

    def reset(self): #returns observations (obs)
        self.env.reset()
        return self.get_state()
        
    def update_game_state(self):
        #pygame function to update entire game display
        pass

    def render(self, mode='human'):
        if mode == 'human':
            self.env.draw_state_pygame()
            time.sleep(self.sleep)

    def close(self):
        pass



def main():
    ## Observation testing
    env = snake_agent_env()
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

