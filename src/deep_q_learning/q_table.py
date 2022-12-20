import numpy as np
import random
import q_table_agent
from gym import Env, spaces

EPISODES = 1000

class QTable:
    def __init__(self, agent=None, alpha=0.2, gamma=0.6, epsilon=1, sleep=0):
        self.alpha = alpha # learning rate
        self.gamma = gamma # discount factor
        self.epsilon = epsilon 
        self.action_space = [0, 1, 2]
        self.observation_space = [[0]*8]*8
        self.q_table = [[[0]*8]*8]*3
        
        self.agent = agent 
        self.init_env(sleep=sleep)

    def init_env(self, sleep=0):
        self.env = q_table_agent.snake_agent_env(sleep=sleep) # later get from self.agent instead


    def choose_action(self, state): #epsilon greedy
        state_f, state_dir = state
        if random.uniform(0, 1) < self.epsilon:
            action = random.choice(self.action_space)
        else:
            actions = [i[state_f][state_dir] for i in self.q_table]
            action = self.action_space[actions.index(max(actions))]
                
        return action

    def perform_action(self, action):
        state, reward, game_over, info = self.env.step(action) # get_reward etc.
        return state, reward, game_over, info

    def update_q_table(self, state, action, new_q_value):
        state_f, state_dir = state
        self.q_table[action][state_f][state_dir] = new_q_value

    def save_q_table(self, path='', name='q_table.txt'):
        with open(path + name, 'w') as f:
            for value in self.q_table:
                f.write(str(value))

    def update_epsilon(self, epsilon):
        self.epsilon = epsilon * 0.9995 #reduce epsilon here
    
        


def train_qtable():
    qtable = QTable()
    for episode in range(EPISODES):
        cur_state = qtable.env.reset()
        game_over = False
        while not game_over:
            action = qtable.choose_action(cur_state)
            state, reward, game_over, info = qtable.perform_action(action)
            state_f, state_dir = state
            old_q_value = qtable.q_table[action][state_f][state_dir]   
            q_max = max([i[state_f][state_dir] for i in qtable.q_table])
            temporal_difference = reward + (qtable.gamma * q_max - old_q_value)
            new_q_value = old_q_value + (qtable.alpha * temporal_difference)
            qtable.update_q_table(cur_state, action, new_q_value)   
            cur_state = state
        print(episode, info)
        qtable.update_epsilon(qtable.epsilon)
    qtable.save_q_table()
    print(qtable.q_table)
    print('Training complete')
    return qtable.q_table

def test_qtable(qtable):
    
    test_env = q_table_agent.snake_agent_env(sleep=0.1)
    state = test_env.reset()
    game_over = False
    reward = 0
    while not game_over:
        test_env.render()
        state_f, state_dir = state
        actions = [i[state_f][state_dir] for i in qtable]
        state, new_reward, game_over, info = test_env.step((max(actions)))
        reward += new_reward
        print(state, reward, game_over, info)
    print(info)
   

q_table = train_qtable()

test_qtable(q_table)
# load qtable array from txt file without numpy


# qtable = []
# with open('q_table.txt', 'r') as f:
#     qtable = f.readlines()
# print(qtable)

