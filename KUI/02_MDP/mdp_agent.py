import random
import copy


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

    return policy


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
    V = {state: 0 for state in states}

    # Initialize the policy for each state to a random action
    policy = {}
    for state in states:
        actions = [action for action in problem.get_actions(state)]

        if problem.is_goal_state(state):
            policy[state] = None
            V[state] = problem.get_reward(state)
        else:
            policy[state] = random.choice(actions)

    # Repeat until the policy converges to the optimal policy

    iteration = 10
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

    return policy
