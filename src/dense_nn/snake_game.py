import random

# THIS SNAKE GAME IS MADE FOR AI TRAINING PURPOSES

# EVERY AGENT I WANT TO TRAIN 
# HAS TO HAVE THE SAME ACTIONS 
# AND THE SAME INPUTS

## THE ACTIONS ARE AS FOLLOWS:
# 0 = move forward
# 1 = turn left
# 2 = turn right

## THE AGENT INPUTS ARE AS FOLLOWS:
# 0 = frame_size [X,Y]
# 1 = snake_head (X,Y)
# 2 = snake_tail [(X,Y), (X,Y), ...]
# 3 = food       (X,Y)   
# 4 = direction  'left', 'right', 'up', 'down'

## GET_STATE FUNCTIONS RETURNS A TUPLE OF ALL THE INPUTS
# (frame_size, snake_head, snake_tail, food, direction)

## PLAY_STEP FUNCTION RETURNS A TUPLE OF THE FOLLOWING:
# (found_food(bool), game_over(bool), game_done(bool), score(int), move_count(int))

# game_done value allready gets returned but is not yet implemented

Frame_size = [15,15]
rand_start_x = random.randint(2,Frame_size[0]-2)
rand_start_y = random.randint(2,Frame_size[1]-2)
Snake_head = (rand_start_x,rand_start_y)
Snake_tail = [(rand_start_x-1,rand_start_y)]
Food = (0,0)
Direction = 'right'

class snake_env():
    def __init__(self, sleep = 0):
        ## AGENT VALUES
        self.action_space = [0,1,2]

        ## GAME VALUES
        self.sleep = sleep
        self.score = 0
        self.move_count = 0
        self.game_over = False
        self.game_done = False

        self.frame_size = Frame_size
        self.snake_head = Snake_head
        self.snake_tail = Snake_tail
        self.food = Food
        self.drop_new_food() 
        self.direction = Direction # left, right, up, down
        
        

        

    def get_state(self):
        return self.frame_size, self.snake_head, self.snake_tail, self.food, self.direction

    def play_step(self, action):
        self.input_to_direction(action)
        next_field = self.get_next_field()
        if self.collision(next_field):
            self.move_count += 1
            self.game_over = True
            return False, True, self.game_done, self.score, self.move_count
        elif self.found_food(next_field):
            self.score += 1
            self.move_count += 1
            self.snake_tail = [self.snake_head] + self.snake_tail
            self.snake_head = next_field
            self.drop_new_food()
            return True, False, self.game_done, self.score, self.move_count
        else:
            self.move_count += 1
            self.snake_tail = [self.snake_head] + self.snake_tail
            self.snake_head = next_field
            self.snake_tail.pop()
            return False, False, self.game_done, self.score, self.move_count

    def draw_state_on_console(self):
        print('__________Score: ', self.score, "___________")
        for y in range(self.frame_size[1]):
            for x in range(self.frame_size[0]):
                if (x,y) == self.snake_head:
                    print('X', end='')
                elif (x,y) in self.snake_tail:
                    print('o', end='')
                elif (x,y) == self.food:
                    print('F', end='')
                else:
                    print('.', end='')
            print()
        print('_________Move_Count: ', self.move_count,'_________\n\n')

    def drop_new_food(self):
        self.food = (random.randint(0,self.frame_size[0]-1), random.randint(0,self.frame_size[1]-1))
        if self.food in self.snake_tail or self.food == self.snake_head:
            self.drop_new_food()

    def get_next_field(self):
        if self.direction == 'right':
            return (self.snake_head[0]+1, self.snake_head[1])
        elif self.direction == 'left':
            return (self.snake_head[0]-1, self.snake_head[1])
        elif self.direction == 'up':
            return (self.snake_head[0], self.snake_head[1]-1)
        elif self.direction == 'down':
            return (self.snake_head[0], self.snake_head[1]+1)

    def collision(self, next_field):
        if next_field in self.snake_tail:
            return True
        elif next_field[0] < 0 or next_field[0] >= self.frame_size[0]:
            return True
        elif next_field[1] < 0 or next_field[1] >= self.frame_size[1]:
            return True
        else:
            return False

    def found_food(self, next_field):
        if next_field == self.food:
            return True
        else:
            return False
    
    def input_to_direction(self, action):
        if self.direction == 'right':
            if action == 0:
                self.direction = 'right'
            elif action == 1:
                self.direction = 'up'
            elif action == 2:
                self.direction = 'down'
        elif self.direction == 'left':
            if action == 0:
                self.direction = 'left'
            elif action == 1:
                self.direction = 'down'
            elif action == 2:
                self.direction = 'up'
        elif self.direction == 'up':
            if action == 0:
                self.direction = 'up'
            elif action == 1:
                self.direction = 'left'
            elif action == 2:
                self.direction = 'right'
        elif self.direction == 'down':
            if action == 0:
                self.direction = 'down'
            elif action == 1:
                self.direction = 'right'
            elif action == 2:
                self.direction = 'left'
    
    def reset(self):
        self.score = 0
        self.move_count = 0
        self.game_over = False
        self.game_done = False
        
        rand_start_x = random.randint(2,Frame_size[0]-2)
        rand_start_y = random.randint(2,Frame_size[1]-2)
         
        self.frame_size = Frame_size
        self.snake_head = (rand_start_x,rand_start_y) 
        self.snake_tail = [(rand_start_x-1,rand_start_y)] 
        self.food = Food
        self.drop_new_food() 
        self.direction = 'right' # left, right, up, down