import snake_game

# Actions are: 0 = forward, 1 = left, 2 = right

# This File is for testing the game logic with user input

new_game = snake_game.snake_env()

def get_user_input(game):
    user_input = input('Enter action: ')
    if user_input == 'w':
        if game.direction == 'up':
            return 0
        elif game.direction == 'down':
            return 0
        elif game.direction == 'left':
            return 2
        elif game.direction == 'right':
            return 1
    elif user_input == 'a':
        if game.direction == 'up':
            return 1
        elif game.direction == 'down':
            return 2
        elif game.direction == 'left':
            return 0
        elif game.direction == 'right':
            return 0
    elif user_input == 's':
        if game.direction == 'up':
            return 0
        elif game.direction == 'down':
            return 0
        elif game.direction == 'left':
            return 1
        elif game.direction == 'right':
            return 2
    elif user_input == 'd':
        if game.direction == 'up':
            return 2
        elif game.direction == 'down':
            return 1
        elif game.direction == 'left':
            return 0
        elif game.direction == 'right':
            return 0
    else:
        return 0

def main():

    game_over = False
    score = 0
    moves = 0

    while game_over == False:
        new_game.draw_state_on_console()
        _,game_over,game_done,score,moves = new_game.play_step(get_user_input(new_game)) 

    print('Game Over! Score: ', score, ' Moves: ', moves)

if __name__ == '__main__':
    main()