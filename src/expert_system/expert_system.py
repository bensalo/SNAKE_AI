import agent_interpreter.agent_2 as agent_2


def calculate_action_simple(observation):
    action_space = [0, 1, 2] # 0 = forward, 1 = left, 2 = right
    action_weights = [0, 0, 0] 
    foodq1 = observation[0]
    foodq2 = observation[1]
    foodq3 = observation[2]
    foodq4 = observation[3]
    collisionfront = observation[4]
    collisionleft = observation[5]
    collisionright = observation[6]
    if foodq1 == 1:
        action_weights[0] += 2
        action_weights[1] += 2
    if foodq2 == 1:
        action_weights[1] += 2
    if foodq3 == 1:
        action_weights[2] += 2
    if foodq4 == 1:
        action_weights[0] += 2
        action_weights[2] += 2
    if collisionfront == 1:
        action_weights[0] -= 5
    if collisionleft == 1:
        action_weights[1] -= 5
    if collisionright == 1:
        action_weights[2] -= 5 
    return action_space[action_weights.index(max(action_weights))]

def calculate_action_medium(observation):
    action_space = [0, 1, 2] # 0 = forward, 1 = left, 2 = right
    action_weights = [0, 0, 0] 
    foodq1 = observation[0]
    foodq2 = observation[1]
    foodq3 = observation[2]
    foodq4 = observation[3]
    collisionfront = observation[4]
    collisionleft = observation[5]
    collisionright = observation[6]
    if foodq1 == 1:
        action_weights[0] += 2
        action_weights[1] += 1
    if foodq2 == 1:
        action_weights[1] += 1
    if foodq3 == 1:
        action_weights[2] += 2
    if foodq4 == 1:
        action_weights[0] += 2
        action_weights[2] += 1
    if collisionfront == 1:
        action_weights[0] -= 5
    if collisionleft == 1:
        action_weights[1] -= 5
    if collisionright == 1:
        action_weights[2] -= 5 
    

def main():
    # Observation testing
    env = agent_2.snake_agent_env(sleep=0.1)
    env.reset()
    reward = 0
    game_over = False
    print("Expert System Snake AI Example")
    env.render()
    observation = env.get_state()
    while not game_over:
        action = calculate_action_simple(observation) ## choose expert system complexity
        observation, step_reward, game_over, info = env.step(action)
        env.render()
        reward += step_reward
        print("Reward: ", reward)

main()