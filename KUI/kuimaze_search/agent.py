import time
import kuimaze
import os
import random
from math import sqrt


class Agent(kuimaze.BaseAgent):
    def __init__(self, environment):
        self.environment = environment

    def find_path(self):
        # getting the information from the environment
        observation = self.environment.reset()
        goal = observation[1][0:2]
        start = observation[0][0:2]

        # intializing evertything needed
        start_node = Node(start, 0, 0, 0, None)
        queue = [start_node]
        already_visited = set()
        path = None

        while queue:
            # choosing a node from queue with the lowest f
            lowest = float("inf")
            for idx, node in enumerate(queue):
                if lowest > node.f:
                    lowest = node.f
                    lowest_idx = idx
            current_node = queue.pop(lowest_idx)

            # checking if the node has the coordinates of the goal
            if current_node.coords == goal:
                print("goal reached")
                path = []
                temp = current_node
                while temp:
                    path.insert(0, temp.coords)
                    temp = temp.parent
                return path

            else:
                # expanding current node
                new_positions = self.environment.expand(current_node.coords)

                # calculating f for every child node
                for pos in new_positions:

                    # pos[0] - coordinates of the node
                    # pos[1] - cost of the node
                    new_node = Node(pos[0], pos[1], 0, 0, current_node)

                    # g is the cost of the path needed to get to the node
                    new_node.g = current_node.g + new_node.cost

                    # h is distance to the goal, using the exact heuristic
                    h = calculate_h(goal, pos[0])

                    new_node.f = new_node.g + h*2

                    # if there is a way to get to point faster than there was before its being changed
                    for idx, node in enumerate(queue):
                        if new_node.coords == node.coords and new_node.f < node.f:
                            queue[idx] = new_node

                    # pushing a node into a queue to expand later
                    if pos[0] not in already_visited:
                        queue.append(new_node)
                        already_visited.add(new_node.coords)

            # render commands
            # self.environment.render()
            # time.sleep(0.1)

        return path


def calculate_h(x, y):
    # function to calculate a distance to the goal
    return sqrt((x[0]-y[0])**2+(x[1]-y[1])**2)


class Node():
    # class for nodes, used to store information
    def __init__(self, coords, cost, f, g, parent=None) -> None:
        self.coords = coords
        self.parent = parent
        self.cost = cost
        self.f = f
        self.g = g


if __name__ == '__main__':

    MAP = 'maps/easy/easy9.bmp'
    MAP = os.path.join(os.path.dirname(os.path.abspath(__file__)), MAP)
    GRAD = (0, 0)
    SAVE_PATH = False
    SAVE_EPS = False

    # For using random map set: map_image=None
    env = kuimaze.InfEasyMaze(map_image=MAP, grad=GRAD)
    agent = Agent(env)

    path = agent.find_path()
    print("path is")

    print(path)
    # set path it should go from the init state to the goal state
    env.set_path(path)
    if SAVE_PATH:
        env.save_path()         # save path of agent to current directory
    if SAVE_EPS:
        env.save_eps()          # save rendered image to eps
    env.render(mode='human')
    time.sleep(3)
