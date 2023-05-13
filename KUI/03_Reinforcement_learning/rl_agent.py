import numpy as np
import time


def learn_policy(env):
    # Hyperparameters
    alpha = 0.1  # Learning rate
    gamma = 0.99  # Discount factor
    epsilon = 0.1  # Exploration rate

    max_steps_per_episode = 1000

    # Extract the dimensions of the state and action spaces
    x_dim = env.observation_space.spaces[0].n
    y_dim = env.observation_space.spaces[1].n
    num_actions = env.action_space.n

    # Initialize the Q-table
    q_table = np.zeros((x_dim, y_dim, num_actions))

    # Set a time limit for learning (in seconds)
    start = time.time()
    while time.time() - start < 19:
        # Reset the environment to the initial state
        state = env.reset()[0:2]
        done = False

        # Iterate through the steps of each episode
        for step in range(max_steps_per_episode):
            # Choose an action using epsilon-greedy strategy
            if np.random.uniform(0, 1) < epsilon:
                action = env.action_space.sample()  # Exploration
            else:
                action = np.argmax(
                    q_table[state[0], state[1], :])  # Exploitation

            # Perform the chosen action and observe the next state, reward, and whether the episode is done
            next_state, reward, done, _ = env.step(action)

            # Update the Q-table using the Q-Learning update rule
            q_table[state[0], state[1], action] = q_table[state[0], state[1], action] + alpha * \
                (reward + gamma * np.max(q_table[next_state[0],
                 next_state[1], :]) - q_table[state[0], state[1], action])

            # Update the current state
            state = next_state

            # Break the loop if the episode is done
            if done:
                break

    # Create the policy as a dictionary
    policy = {}
    for x in range(x_dim):
        for y in range(y_dim):
            state = (x, y)
            best_action = np.argmax(q_table[x, y, :])
            policy[state] = best_action

    return policy  # Return the learned policy
