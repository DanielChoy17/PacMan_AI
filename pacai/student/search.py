"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""

from pacai.util.stack import Stack
from pacai.util.queue import Queue
from pacai.util.priorityQueue import PriorityQueue

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first [p 85].

    Your search algorithm needs to return a list of actions that reaches the goal.
    Make sure to implement a graph search algorithm [Fig. 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    ```
    print("Start: %s" % (str(problem.startingState())))
    print("Is the start a goal?: %s" % (problem.isGoal(problem.startingState())))
    print("Start's successors: %s" % (problem.successorStates(problem.startingState())))
    ```
    """
    # Storing the starting node into variable node
    node = problem.startingState()
    # Checking to to see if the starting node is the goal else do DFS Algorithm to find path to goal
    if problem.isGoal(problem.startingState()):
        return node
    else:
        # Stack to store the nodes with their corresponding paths
        fringe = Stack()
        # Pushing the starting node into the fringe
        fringe.push((problem.startingState(), []))
        # Set to store all the visited nodes
        reached = set()
        # Adding the starting node to reached set
        reached.add(node)
        while not fringe.isEmpty():
            temp = fringe.pop()
            node = temp[0]
            path_to_node = temp[1]
            # Getting the successors of the popped node
            successors = problem.successorStates(node)
            # Iterating through all the successors of the popped node
            for successor in successors:
                successor_node = successor[0]
                successor_path = successor[1]
                # Creating the path from the starting node to the current successor node
                successor_full_path = path_to_node + [successor_path]
                # Return the full path if the goal node is reached
                if problem.isGoal(successor_node):
                    return successor_full_path
                # Checking to see if the current successor node is in the reached set
                if successor_node not in reached:
                    # Adding the current successor node to the reached set
                    reached.add(successor_node)
                    # Pushing the current successor node and its corresponding path to the fringe
                    fringe.push((successor_node, successor_full_path))

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """
    # Storing the starting node into variable node
    node = problem.startingState()
    # Checking to to see if the starting node is the goal else do BFS Algorithm to find path to goal
    if problem.isGoal(problem.startingState()):
        return node
    else:
        # Queue to store the nodes with their corresponding paths
        fringe = Queue()
        # Pushing the starting node into the fringe
        fringe.push((problem.startingState(), []))
        # Set to store all the visited nodes
        reached = set()
        # Adding the starting node to reached set
        reached.add(node)
        while not fringe.isEmpty():
            temp = fringe.pop()
            node = temp[0]
            path_to_node = temp[1]
            # Getting the successors of the popped node
            successors = problem.successorStates(node)
            # Iterating through all the successors of the popped node
            for successor in successors:
                successor_node = successor[0]
                successor_path = successor[1]
                # Creating the path from the starting node to the current successor node
                successor_full_path = path_to_node + [successor_path]
                # Return the full path if the goal node is reached
                if problem.isGoal(successor_node):
                    return successor_full_path
                # Checking to see if the current successor node is in the reached set
                if successor_node not in reached:
                    # Adding the current successor node to the reached set
                    reached.add(successor_node)
                    # Pushing the current successor node and its corresponding path to the fringe
                    fringe.push((successor_node, successor_full_path))

def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """
    # Storing the starting node into variable node
    node = problem.startingState()
    # Checking to to see if the starting node is the goal else do UCS Algorithm to find path to goal
    if problem.isGoal(problem.startingState()):
        return node
    else:
        # Priority Queue to store the nodes with their corresponding paths, full costs, and priority
        fringe = PriorityQueue()
        # Pushing the starting node into the fringe
        fringe.push((problem.startingState(), [], 0), 0)
        # Set to store all the visited nodes
        reached = set()
        # Adding the starting node to reached set
        reached.add(node)
        while not fringe.isEmpty():
            temp = fringe.pop()
            node = temp[0]
            path_to_node = temp[1]
            cost_to_node = temp[2]
            # Getting the successors of the popped node
            successors = problem.successorStates(node)
            # Iterating through all the successors of the popped node
            for successor in successors:
                successor_node = successor[0]
                successor_path = successor[1]
                successor_cost = successor[2]
                # Creating the path from the starting node to the current successor node
                successor_full_path = path_to_node + [successor_path]
                # Calculating the cost from the starting node to the current successor node
                successor_full_cost = cost_to_node + successor_cost
                # Return the full path if the goal node is reached
                if problem.isGoal(successor_node):
                    return successor_full_path
                # Checking to see if the current successor node is in the reached set
                if successor_node not in reached:
                    # Adding the current successor node to the reached set
                    reached.add(successor_node)
                    # Pushing the current successor node, its corresponding path, its
                    # full cost, and priority to the fringe
                    fringe.push((successor_node, successor_full_path,
                                 successor_full_cost), successor_full_cost)

def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    # Storing the starting node into variable node
    node = problem.startingState()
    # Checking to to see if the starting node is the goal else do A* Algorithm to find path to goal
    if problem.isGoal(problem.startingState()):
        return node
    else:
        # Priority Queue to store the nodes with their corresponding paths, full costs, and priority
        fringe = PriorityQueue()
        # Pushing the starting node into the fringe
        fringe.push((problem.startingState(), [], 0),
                    0 + heuristic(problem.startingState(), problem))
        # Set to store all the visited nodes
        reached = set()
        # Adding the starting node to reached set
        reached.add(node)
        while not fringe.isEmpty():
            temp = fringe.pop()
            node = temp[0]
            path_to_node = temp[1]
            cost_to_node = temp[2]
            # Getting the successors of the popped node
            successors = problem.successorStates(node)
            # Iterating through all the successors of the popped node
            for successor in successors:
                successor_node = successor[0]
                successor_path = successor[1]
                successor_cost = successor[2]
                # Creating the path from the starting node to the current successor node
                successor_full_path = path_to_node + [successor_path]
                # Calculating the cost from the starting node to the current successor node
                successor_full_cost = cost_to_node + successor_cost
                # Return the full path if the goal node is reached
                if problem.isGoal(successor_node):
                    return successor_full_path
                # Checking to see if the current successor node is in the reached set
                if successor_node not in reached:
                    # Adding the current successor node to the reached set
                    reached.add(successor_node)
                    # Pushing the current successor node, its corresponding path,
                    # its full cost, and priority to the fringe
                    fringe.push((successor_node, successor_full_path, successor_full_cost),
                                successor_full_cost + heuristic(successor_node, problem))
