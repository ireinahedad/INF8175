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

from custom_types import Direction
from pacman import GameState
from typing import Any, Tuple,List
import util
import queue

"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self)->Any:
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state:Any)->bool:
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state:Any)->List[Tuple[Any,Direction,int]]:
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions:List[Direction])->int:
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()



def tinyMazeSearch(problem:SearchProblem)->List[Direction]:
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem:SearchProblem)->List[Direction]:
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:


    """

    stack = []

    start = problem.getStartState()
    stack.append((start, []))
    visited = set()

    while stack:
        # Pop the last element from the stack
        state, path = stack.pop()

        if problem.isGoalState(state):
            return path

        # If we have not visited this state yet, expand it
        if state not in visited:
            visited.add(state)

            # Expand the state and push the successors onto the stack
            for next_state, action, step_cost in problem.getSuccessors(state):
                new_path = path + [action]  # Append the action to the current path
                stack.append((next_state, new_path))

    return []
    util.raiseNotDefined()


def breadthFirstSearch(problem:SearchProblem)->List[Direction]:
    """Search the shallowest nodes in the search tree first."""

    q = queue.Queue()

    start = problem.getStartState()
    q.put((start, []))
    visited = set()

    while not q.empty():
        state, path = q.get()

        if problem.isGoalState(state):
            return path

        if state not in visited:
            visited.add(state)

            for next_state, action, step_cost in problem.getSuccessors(state):
                new_path = path + [action]  # Append the action to the current path
                q.put((next_state, new_path))

    return []
    util.raiseNotDefined()

def uniformCostSearch(problem:SearchProblem)->List[Direction]:
    """Search the node of least total cost first."""

    priorityQ = util.PriorityQueue()

    start = problem.getStartState()
    priorityQ.push((start, [], 0), 0)  # (state, path, cumulative cost)

    # Set to track visited states and their costs
    visited = {}

    while not priorityQ.isEmpty():
        # Pop state with  lowest cost
        state, path, cost = priorityQ.pop()

        if problem.isGoalState(state):
            return path

        if state not in visited or visited[state] > cost:
            visited[state] = cost  # Mark this state as visited with the current cost

            for next_state, action, step_cost in problem.getSuccessors(state):
                new_cost = cost + step_cost
                new_path = path + [action]
                priorityQ.push((next_state, new_path, new_cost), new_cost)


    return []
    util.raiseNotDefined()

def nullHeuristic(state:GameState, problem:SearchProblem=None)->List[Direction]:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem:SearchProblem, heuristic=nullHeuristic)->List[Direction]:
    """Search the node that has the lowest combined cost and heuristic first."""
    priorityQ = util.PriorityQueue()

    start = problem.getStartState()

    priorityQ.push((start, [], 0), 0)  # (state, path, cost)
    visited = {}

    while not priorityQ.isEmpty():
        # Pop state avec lowest cost
        state, path, g_cost = priorityQ.pop()

        if problem.isGoalState(state):
            return path


        if state not in visited or visited[state] > g_cost:
            visited[state] = g_cost


            for next_state, action, step_cost in problem.getSuccessors(state):
                new_g_cost = g_cost + step_cost
                h_cost = heuristic(next_state, problem)
                f_cost = new_g_cost + h_cost
                new_path = path + [action]


                priorityQ.push((next_state, new_path, new_g_cost), f_cost)


    return []

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
