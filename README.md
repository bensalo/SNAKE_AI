# SNAKE_AI

Welcome to my Snake Gym! Here i want to train different machine learning Agents to play the Game of Snake. Notice that some Agents are still in Progress!

I wanted to make the Snake Game from Scratch so i did. I want to build my Gym very modular for good comparisons at the end. 

First there is the Snake Game itself, with every needed Information. 

Than i have a Agent_Interpreter (Agent 1, Agent 2 or Agent_Interpreter) which takes every game information from the game itself and calculates the observations for the Agent. I want to try different observation values, thats why i made this a class, to easy swap them afterwards.

After the Agent Interpreter is the Agent itself. Right now i have a working expert System with a record ~20 and a Q-learning Agent with a record of ~45.

After the Agent is (except for the expert System) a model.  In future i want to try different libraries for machine learning (tensorflow is next) and also a Q learning Table without any machine learning library. (NumPy only :))

To replay the record runs in a Snake Game, simply open runs/play_run.py and insert the run you want to play in line 30.
Noitice: you need to have pygame, numpy and time installed. I have a graphical User Interface Planned to see the record of different Agents after x hours of training.
