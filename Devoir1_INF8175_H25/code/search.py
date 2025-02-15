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

# Noms et matricules des membres de l'équipe:
# - Ireina Hedad - 2213673
# - Thomas Rouleau - 2221053


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from custom_types import Direction
from pacman import GameState
from typing import Any, Tuple,List
import util

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

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """

    initial_state = problem.getStartState()
    if problem.isGoalState(initial_state):
        return []

    pathStack = util.Stack()
    pathStack.push((initial_state, []))
    visited = set()

    while not pathStack.isEmpty():
        current_state, actions = pathStack.pop()

        if current_state in visited:
            continue

        visited.add(current_state)

        if problem.isGoalState(current_state):
            return actions

        for successor, action, _ in problem.getSuccessors(current_state):
            if successor not in visited:
                pathStack.push((successor, actions + [action]))

    util.raiseNotDefined()


def breadthFirstSearch(problem:SearchProblem)->List[Direction]:
    """Search the shallowest nodes in the search tree first."""

    initial_state = problem.getStartState()
    if problem.isGoalState(initial_state):
        return []

    pathQueue = util.Queue()
    pathQueue.push((initial_state, []))
    visited = set()

    while not pathQueue.isEmpty():
        current_state, actions = pathQueue.pop()

        if current_state in visited:
            continue

        visited.add(current_state)

        print(current_state)

        if problem.isGoalState(current_state):
            return actions

        for successor, action, _ in problem.getSuccessors(current_state):
                if successor not in visited:
                    pathQueue.push((successor, actions + [action]))

    util.raiseNotDefined()

def uniformCostSearch(problem:SearchProblem)->List[Direction]:
    """Search the node of least total cost first."""


    '''
        INSÉREZ VOTRE SOLUTION À LA QUESTION 3 ICI
    '''

    initial_state = problem.getStartState()
    if problem.isGoalState(initial_state):
        return []

    print("path", initial_state)

    pathPriorityQueue = util.PriorityQueue()
    initial_weight = 0
    pathPriorityQueue.push((initial_state, []), initial_weight)
    visited = set()
    current_cost = {initial_state: 0}

    while not pathPriorityQueue.isEmpty():
        current_state, actions = pathPriorityQueue.pop()

        if current_state in visited:
            continue

        visited.add(current_state)

        if problem.isGoalState(current_state):
            return actions

        for successor, action, step_cost in problem.getSuccessors(current_state):
            cost = current_cost[current_state] + step_cost
            if successor not in current_cost or cost < current_cost[successor]:
                current_cost[successor] = cost
                pathPriorityQueue.push((successor, actions + [action]), cost)

    util.raiseNotDefined()

def nullHeuristic(state:GameState, problem:SearchProblem=None)->List[Direction]:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem:SearchProblem, heuristic=nullHeuristic)->List[Direction]:
    """Search the node that has the lowest combined cost and heuristic first."""
    '''
        INSÉREZ VOTRE SOLUTION À LA QUESTION 4 ICI
    '''
    initial_state = problem.getStartState()
    if problem.isGoalState(initial_state):
        return []

    pathPriorityQueue = util.PriorityQueue()
    initial_weight = heuristic(initial_state, problem)
    pathPriorityQueue.push((initial_state, []), initial_weight)

    visited = set()
    current_cost = {initial_state: 0}

    while not pathPriorityQueue.isEmpty():
        current_state, actions = pathPriorityQueue.pop()
        if current_state in visited:
            continue

        visited.add(current_state)

        if problem.isGoalState(current_state):
            return actions

        for successor, action, step_cost in problem.getSuccessors(current_state):
            cost = current_cost[current_state] + step_cost
            heuristic_cost = cost + heuristic(successor, problem)
            if successor not in current_cost or cost < current_cost[successor]:
                current_cost[successor] = cost
                pathPriorityQueue.push((successor, actions + [action]), heuristic_cost)

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
