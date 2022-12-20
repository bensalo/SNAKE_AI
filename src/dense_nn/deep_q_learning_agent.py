import torch
import random
import numpy as np
import time
from collections import deque
from deep_q_learning_model import Linear_QNet, QTrainer
import agent_interpreter
from matplotlib import pyplot as plt

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.0012

class Agent:
    def __init__(self):
        self.n_game = 0
        self.epsilon = 0.1 # Randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(11,256,3)
        self.model.to('cuda')
        self.trainer = QTrainer(self.model,lr=LR,gamma=self.gamma)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))   # popleft if MAX_MEMORY is reached
    
    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
    
    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)
    
    def get_action(self, state):
        self.epsilon = 80 - self.n_game
        final_move = [0,0,0]
        if(random.randint(0,200)<self.epsilon):
            move = random.randint(0,2)
            final_move[move]=1
        else:
            state0 = torch.tensor(state,dtype=torch.float).cuda()
            prediction = self.model(state0).cuda() # prediction by model 
            move = torch.argmax(prediction).item()
            final_move[move]=1 
        return final_move


def play_record_run(name): # takes smth like record_run_2
    path = 'runs/' + name +'.npy'
    run = np.load(path, allow_pickle=True)
    game = agent_interpreter.dq_agent_interpreter(sleep=0.1)
    for (state) in run:
        game.render_state(state)
        time.sleep(0.2)
        
    game.reset()

def save_record_run(run, score):
    path = 'runs/record_run_' + str(score) +'.npy'
    run = np.array(run, dtype=object)
    np.save(path, run)


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = agent_interpreter.dq_agent_interpreter(sleep=0) # if sleep > 0 then game will be rendered
    run = []
    record_run = []
    while agent.n_game < 200 and record < 42:
        # Save state 
        run.append(game.env.get_state())
        # Get Old state
        state_old = game.get_state()
        # get move
        final_move = agent.get_action(state_old)
        # perform move and get new state
        reward, done, score = game.step(final_move)
        game.render() # anythin else as 'human' will not render the game
        state_new = game.get_state()
        # train short memory
        agent.train_short_memory(state_old,final_move,reward,state_new,done)

        #remember
        agent.remember(state_old,final_move,reward,state_new,done)

        if done:
            # save last state
            run.append(game.env.get_state())
            # Train long memory,plot result
            game.reset()
            agent.n_game += 1
            agent.train_long_memory()
            if(score > record): # new High score 
                record = score
                record_run.clear()
                record_run = run.copy()
                run.clear()
                run = []
            else:
                run.clear()
                run = []
            print('Game:',agent.n_game,'Score:',score,'Record:',record)
            
            plot_scores.append(score)
            total_score+=score
            mean_score = total_score / agent.n_game
            plot_mean_scores.append(mean_score)
    
    agent.model.save()
    save_record_run(record_run, record)
            
def test_model():
    agent = Agent()
    agent.model.load_state_dict(torch.load('C:\CODING\PROJECTS\SNAKE_AI\models\dql_model.pth'))
    game = agent_interpreter.dq_agent_interpreter(sleep=0.1)
    while True:
        # Get Old state
        state_old = game.get_state()

        # get move
        final_move = agent.get_action(state_old)
        # perform move and get new state
        reward, done, score = game.step(final_move)
        game.render() # anythin else as 'human' will not render the game
        state_new = game.get_state()

        if done:
            # Train long memory,plot result
            game.reset()
            agent.n_game += 1
            print('Game:',agent.n_game,'Score:',score)
            if(score > 40):
                break



if(__name__=="__main__"):
    
    #train()
    #test_model()
    play_record_run('record_run_46')
    #pass
    
