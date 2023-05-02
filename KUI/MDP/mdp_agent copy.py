import numpy as np

import random
import os
import time
import sys
import copy

import kuimaze
from kuimaze import keyboard, State


MAP = "maps/easy/easy4.bmp"
MAP = os.path.join(os.path.dirname(os.path.abspath(__file__)), MAP)
PROBS = [0.8, 0.1, 0.1, 0]
GRAD = (0, 0)
keyboard.SKIP = False
SAVE_EPS = False
VERBOSITY = 2


GRID_WORLD4 = [
    [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 0, 0]],
    [[255, 255, 255], [0, 0, 0], [255, 255, 255], [255, 255, 255]],
    [[0, 0, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]],
    [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]],
]

GRID_WORLD3 = [
    [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 0, 0]],
    [[255, 255, 255], [0, 0, 0], [255, 255, 255], [255, 0, 0]],
    [[0, 0, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]],
]

REWARD_NORMAL_STATE = -0.04
REWARD_GOAL_STATE = 1
REWARD_DANGEROUS_STATE = -1

GRID_WORLD3_REWARDS = [
    [REWARD_NORMAL_STATE, REWARD_NORMAL_STATE,
        REWARD_NORMAL_STATE, REWARD_GOAL_STATE],
    [REWARD_NORMAL_STATE, 0,
        REWARD_NORMAL_STATE, REWARD_DANGEROUS_STATE],
    [REWARD_NORMAL_STATE, REWARD_NORMAL_STATE,
        REWARD_NORMAL_STATE, REWARD_NORMAL_STATE],
]


def get_visualisation_values(dictvalues):
    if dictvalues is None:
        return None
    ret = []
    for key, value in dictvalues.items():
        # ret.append({'x': key[0], 'y': key[1], 'value': [value, value, value, value]})
        ret.append({"x": key[0], "y": key[1], "value": value})
    return ret


"""
def find_policy_via_value_iteration(problem, gamma, epsilon):

    def action_value_val_iter(state, action, V):
        value = 0
        next_states = problem.get_next_states_and_probs(state, action)

        for next_state, probability in next_states:
            value += probability * V[next_state]

        return value

    def get_optimal_action(state, V):
        best_action = None
        best_value = float('-inf')
        actions = [action for action in problem.get_actions(state)]

        for action in actions:
            action_value = action_value_val_iter(state, action, V)
            if action_value > best_value:
                best_value = action_value
                best_action = action
        return best_action

    states = problem.get_all_states()
    V = {state: 0 for state in states}
    policy = {state: None for state in states}

    while True:
        delta = 0
        for state in states:
            if problem.is_goal_state(state):
                V[state] = problem.get_reward(state)
                continue

            old_value = V[state]

            actions = [action for action in problem.get_actions(state)]

            cur_value = float('-inf')
            for action in actions:
                action_value = action_value_val_iter(state, action, V)
                cur_value = max(action_value, cur_value)

            V[state] = problem.get_reward(state) + gamma * cur_value

            delta = max(delta, abs(old_value - V[state]))

        if delta < (epsilon*(1-gamma))/gamma:
            break

    for state in states:
        if not problem.is_goal_state(state):
            policy[state] = get_optimal_action(state, V)

    return policy, V


def find_policy_via_policy_iteration(problem, gamma):

    def action_value_pol_iter(state, action, V):
        value = 0
        next_states = problem.get_next_states_and_probs(state, action)

        for next_state, probability in next_states:
            reward = problem.get_reward(next_state)
            value += probability * (reward + gamma * V[next_state])

        return value

    def policy_evaluation(policy, V, problem):
        V_copy = copy.copy(V)

        for state in states:
            if not problem.is_goal_state(state):
                # V_copy[state] = action_value_pol_iter(state, policy[state], V)\
                next_states = problem.get_next_states_and_probs(
                    state, policy[state])
                new_value = 0
                for next_state, probability in next_states:
                    reward = problem.get_reward(next_state)
                    new_value += probability * (reward + gamma * V[next_state])

                V_copy[state] = new_value

        return V_copy

    states = problem.get_all_states()

    policy = {}
    # V = {state: 0 for state in states}
    V = {}
    for state in states:
        actions = [action for action in problem.get_actions(state)]

        if problem.is_goal_state(state):
            policy[state] = None
            V[state] = problem.get_reward(state)
        else:
            policy[state] = random.choice(actions)
            V[state] = 0

    changed = True
    while changed:
        changed = False

        V = policy_evaluation(policy, V, problem)
        print(V)
        for state in states:
            if problem.is_goal_state(state):
                continue

            actions = [action for action in problem.get_actions(state)]
            best_value = float('-inf')
            best_action = None
            for action in actions:
                action_value = action_value_pol_iter(state, action, V)
                if action_value > best_value:
                    best_value = action_value
                    best_action = action

            policy_action_value = action_value_pol_iter(
                state, policy[state], V)

            if best_value > policy_action_value:
                policy[state] = best_action
                changed = True

    return policy, V
"""


def find_policy_via_value_iteration(problem, gamma, epsilon):

    def action_value_val_iter(state, action, V):
        """
        Computes the value of a state-action pair
        for value iteration algorithm
        """

        value = 0
        next_states = problem.get_next_states_and_probs(state, action)

        for next_state, probability in next_states:
            value += probability * V[next_state]

        return value

    def get_optimal_action(state, V):
        """
        Finds the optimal action for a given state
        """

        best_action = None
        best_value = float('-inf')
        actions = [action for action in problem.get_actions(state)]

        for action in actions:
            action_value = action_value_val_iter(state, action, V)
            if action_value > best_value:
                best_value = action_value
                best_action = action
        return best_action

    # Initialize the value estimates for each state to zero
    states = problem.get_all_states()
    V = {state: 0 for state in states}

    # Initialize the policy for each state to None
    policy = {state: None for state in states}

    # Repeat until the maximum error is below the specified epsilon
    while True:
        delta = 0
        for state in states:
            if problem.is_goal_state(state):
                # If the state is a goal state, set its value to its reward
                V[state] = problem.get_reward(state)
                continue
            # Keep a copy of the old value estimate for the state
            old_value = V[state]

            # Find the action that maximizes the value of the state-action pair
            actions = [action for action in problem.get_actions(state)]
            current_value = float('-inf')
            for action in actions:
                action_value = action_value_val_iter(state, action, V)
                current_value = max(action_value, current_value)

            # Update the value estimate for the state using the Bellman equation
            V[state] = problem.get_reward(state) + gamma * current_value

            # Update delta to keep track of the maximum change in the value estimates
            delta = max(delta, abs(old_value - V[state]))

        # If the maximum error is below the specified epsilon, terminate the algorithm
        if delta < (epsilon*(1-gamma))/gamma:
            break

    # For each state, find the optimal action and store it in the policy
    for state in states:
        if not problem.is_goal_state(state):
            policy[state] = get_optimal_action(state, V)

    return policy, V


def find_policy_via_policy_iteration(problem, gamma):

    def action_value_pol_iter(state, action, V):
        """
        Computes the value of a state-action pair
        for policy iteration algorithm
        """

        value = 0
        next_states = problem.get_next_states_and_probs(state, action)

        for next_state, probability in next_states:
            reward = problem.get_reward(next_state)
            value += probability * (reward + gamma * V[next_state])

        return value

    def policy_evaluation(policy, V, problem):
        """
        Evaluates the given policy and
        updates the value estimates for each state
        """

        # Make a copy of the current value estimates
        V_copy = copy.copy(V)

        # For each non-goal state, update the value estimate using the Bellman equation
        for state in states:
            if not problem.is_goal_state(state):
                next_states = problem.get_next_states_and_probs(
                    state, policy[state])
                new_value = 0
                for next_state, probability in next_states:
                    reward = problem.get_reward(next_state)
                    new_value += probability * (reward + gamma * V[next_state])

                V_copy[state] = new_value

        return V_copy
    # Initialize the value estimates for each state to zero
    states = problem.get_all_states()
    # V = {state: problem.get_reward(state) for state in states}
    V = {state: 0 for state in states}

    # Initialize the policy for each state to a random action
    policy = {}
    for state in states:
        actions = [action for action in problem.get_actions(state)]

        if problem.is_goal_state(state):
            policy[state] = None
            V[state] = problem.get_reward(state)
        else:
            # policy[state] = random.choice(actions)
            policy[state] = actions[0]

    # Repeat until the policy converges to the optimal policy
    iteration = 2
    while iteration != 0:
        changed = False
        # Evaluate the current policy and update the value estimates for each state
        V = policy_evaluation(policy, V, problem)

        # For each non-goal state, find the action that maximizes the value of the state-action pair
        for state in states:
            if problem.is_goal_state(state):
                continue

            actions = [action for action in problem.get_actions(state)]
            best_value = float('-inf')
            best_action = None
            for action in actions:
                action_value = action_value_pol_iter(state, action, V)
                if action_value > best_value:
                    best_value = action_value
                    best_action = action

            policy_action_value = action_value_pol_iter(
                state, policy[state], V)

            # If a better action is found, update the policy and set changed to True
            if best_value > policy_action_value:
                policy[state] = best_action
                changed = True

        if not changed:
            iteration -= 1

    return policy, V


if __name__ == "__main__":
    # Initialize the maze environment
    env = kuimaze.MDPMaze(
        map_image=GRID_WORLD3, probs=PROBS, grad=GRAD, node_rewards=GRID_WORLD3_REWARDS
    )
    # env = kuimaze.MDPMaze(map_image=GRID_WORLD3, probs=PROBS, grad=GRAD, node_rewards=None)
    env = kuimaze.MDPMaze(map_image=MAP, probs=PROBS,
                          grad=GRAD, node_rewards=None)
    env.reset()

    print("====================")
    print("press n - next")
    print("press s - skip to end")
    print("====================")

    print(env.get_all_states())
    states = env.get_all_states()
    utils = {state: env.get_reward(state) for state in states}
    # policy, V = find_policy_via_value_iteration(env, 0.999999, 0.03)
    policy, V = find_policy_via_policy_iteration(env, 0.999)
    print(V)
    env.visualise(get_visualisation_values(policy))
    env.render()
    keyboard.wait_n_or_s()
    print("Policy:", policy)
    # env.visualise(get_visualisation_values(utils))
    env.visualise(get_visualisation_values(V))
    env.render()
    time.sleep(1)
