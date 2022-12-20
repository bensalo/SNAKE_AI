import agent_interpreter.agent_1 as agent_1
import agent_interpreter.agent_2 as agent_2
import random
import numpy as np
from gym import spaces

## create q table agent ##
## snake env ##
## observation space = 5
## snake head x, snake head y, food x, food y, direction

## action space = 3
## [0,1,2] = [straight, left, right]

## VARIABLES ##
LEARNING_RATE = 0.1
DISCOUNT = 0.95
EPISODES = 10000
SHOW_EVERY = 1000
MIN_EPSILON = 0.001
MAX_EPSILON = 1
DECAY_RATE = 0.0001
epsilon = 1
discrete_os_win_size = [20, 20, 20, 20, 4]

def main():
    env = agent_1.snake_agent_env()
    q_table = create_q_table()
    for episode in range(EPISODES):
        state = env.reset()
        done = False
        score = 0
        while not done:
            action = get_action(q_table, state, env.action_space)
            new_state, reward, done, info = env.step(action)
            new_q = get_new_q_value(q_table, state, action, reward, new_state, done)
            q_table = update_q_table(q_table, state, action, new_q)
            state = new_state
            score += reward
        epsilon = get_epsilon(episode)
        print("Episode: {}, Score: {}, Epsilon: {}".format(episode, score, epsilon))
    return q_table

def create_q_table():
    q_table = np.zeros((5, 5, 5, 5, 4, 3))
    return q_table

def get_discrete_state(state, env):
    discrete_state = (state - env.observation_space.low) / discrete_os_win_size
    return tuple(discrete_state.astype(np.int))

def get_action(q_table, state, action_space):
    if random.random() > epsilon:
        action = np.argmax(q_table[state])
        print(q_table[state])
    else:
        action = np.random.randint(0, action_space.n)
    return action

def get_new_q_value(q_table, state, action, reward, new_state, done):
    if not done:
        max_future_q = np.max(q_table[new_state])
        new_q = (1 - LEARNING_RATE) * q_table[state + (action,)] + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
    else:
        new_q = (1 - LEARNING_RATE) * q_table[state + (action,)] + LEARNING_RATE * (reward)
    return new_q

def update_q_table(q_table, state, action, new_q):
    q_table[state + (action,)] = new_q
    return q_table

def get_epsilon(episode):
    epsilon = MIN_EPSILON + (MAX_EPSILON - MIN_EPSILON) * np.exp(-DECAY_RATE * episode)
    return epsilon

# save q table as txt
with open('q_table.txt', 'w') as f:
    for item in main():
        f.write(item)
