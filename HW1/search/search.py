# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    startState = problem.getStartState()

    s = util.Stack()
    expanded = []

    # Keeping the state - path to arrive this state as key value pairs in the stack
    s.push((startState, []))

    while not s.isEmpty():
        cur = s.pop()
        key_state, path_val = cur

        if key_state in expanded:
            continue

        if problem.isGoalState(key_state):
            return path_val

        expanded.append(key_state)
        for next_state, facing_direction, action_cost in problem.getSuccessors(key_state):
            s.push((next_state, path_val + [facing_direction]))



def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    startState = problem.getStartState()

    # The only difference is that we use queue instead of a stack.
    q = util.Queue()
    expanded = []

    # Keeping the state - path to arrive this state as key value pairs in the queue this time.
    q.push((startState, []))

    while not q.isEmpty():
        cur = q.pop()
        key_state, path_val = cur

        if key_state in expanded:
            continue

        if problem.isGoalState(key_state):
            return path_val

        expanded.append(key_state)
        for next_state, facing_direction, action_cost in problem.getSuccessors(key_state):
            q.push((next_state, path_val + [facing_direction]))


def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    startState = problem.getStartState()

    pq = util.PriorityQueue()
    expanded = []

    # Since pop operation only returns the item but not the priority, we should also keep track of priority
    pq.push((startState, ([], 0)), 0)
    # Each element of priority queue is a path-cost tuple indexed by the state

    while not pq.isEmpty():
        cur = pq.pop()
        key_state, tuple = cur
        path_val, priority = tuple

        if key_state in expanded:
            continue

        if problem.isGoalState(key_state):
            return path_val

        expanded.append(key_state)
        # As path gets longer, priority value increases; priority in min heeap decreases
        for next_state, facing_direction, action_priority in problem.getSuccessors(key_state):
            pq.push((next_state, (
                    path_val + [facing_direction], priority + action_priority)), priority + action_priority)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    startState = problem.getStartState()

    pq = util.PriorityQueue()

    expanded = []

    pq.push((startState, ([], 0)), 0)

    while not pq.isEmpty():
        cur = pq.pop()
        key_state, tuple = cur
        path_val, priority = tuple

        if key_state in expanded:
            continue

        if problem.isGoalState(key_state):
            return path_val

        expanded.append(key_state)
        for next_state, facing_direction, action_priority in problem.getSuccessors(key_state):
            g = priority + action_priority
            f = heuristic(next_state, problem) + g
            pq.push((next_state, (
                    path_val + [facing_direction], g)), f)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
