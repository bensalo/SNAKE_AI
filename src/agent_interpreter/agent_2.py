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

# the get_obs function returns a list of 7 values:
# 

# Currently Used for the Expert System!

class snake_agent_env(gym.Env):

    metadata = {'render.modes': ['human']}

    def __init__(self, sleep=0):
        self.env = snake_game.snake_env()
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(low=0, high=1, shape=(7,), dtype=np.int0)
        self.sleep = sleep
        self.env.reset()
        ## pygame stuff
        #self.update_game_state()
        

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
        
        return [foodq1,foodq2,foodq3,foodq4,collisionfront,collisionleft,collisionright]

    def get_state(self):
        frame_size, snake_head, snake_tail, food, dir = self.env.get_state()
        return self.get_obs(frame_size, snake_head, snake_tail, food, dir)

    def calc_reward(self, pre_state, found_food, game_over, game_done):
        reward = 0
        frame_size, snake_head, snake_tail, food, dir = self.env.get_state()
        _, pre_snake_head, _, _, _ = pre_state
        euclid_head_food = math.sqrt((food[0] - snake_head[0]) ** 2 + (food[1] - snake_head[1]) ** 2)
        euclid_pre_head_food = math.sqrt((food[0] - pre_snake_head[0]) ** 2 + (food[1] - pre_snake_head[1]) ** 2)
        if euclid_head_food < euclid_pre_head_food:
            reward += 2
        else:
            reward -= 1


        if found_food:
            reward += 20
        if game_over:
            reward -= 20
        return reward

    def step(self, action):
        pre_state = self.env.get_state()
        found_food, game_over, game_done, score, move_count = self.env.play_step(action)
        reward = self.calc_reward(pre_state,found_food, game_over, game_done)
        info = {'score': score, 'move_count': move_count}
        time.sleep(self.sleep)
        return self.get_state(), reward, game_done or game_over, info

    def reset(self):
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

