import pygame
import numpy as np
import time

def play_record_run(name): # takes smth like record_run_2
    path = 'runs/' + name +'.npy'
    run = np.load(path, allow_pickle=True)
    pygame.init()
    for (state) in run:
        render_state(state)
        time.sleep(0.2)
        
def render_state(state):
    frame_size, snake_head, snake_tail, food, direction = state
    screen = pygame.display.set_mode((frame_size[0]*50, frame_size[1]*50))
    screen.fill((0,0,0))
    for y in range(frame_size[1]):
        for x in range(frame_size[0]):
            if (x,y) == snake_head:
                pygame.draw.rect(screen, (255,0,0), (x*50,y*50,50,50))
            elif (x,y) in snake_tail:
                pygame.draw.rect(screen, (0,255,0), (x*50,y*50,50,50))
            elif (x,y) == food:
                pygame.draw.rect(screen, (0,0,255), (x*50,y*50,50,50))
            else:
                pygame.draw.rect(screen, (255,255,255), (x*50,y*50,50,50), 1)
    pygame.display.update()

def main():
    play_record_run('record_run_46') #insert the name of the run here!

main()