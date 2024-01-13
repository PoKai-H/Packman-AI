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
    return  [s, s, w, s, w, w, s, w]

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
    start = problem.getStartState()
    coor = problem.getStartState()
    explored = []
    explored.append(start)
    fringe = util.Stack()
    stack_tuple = (start, [])
    fringe.push(stack_tuple)
    while not fringe.isEmpty() and not problem.isGoalState(coor):
        state, actions = fringe.pop()
        explored.append(state)
        successor = problem.getSuccessors(state)
        for i in successor:
            coordinates = i[0]
            if not coordinates in explored:
                coor = i[0]
                direction = i[1]
                fringe.push((coor, actions +[direction]))
    
    return actions+[direction]
    util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    
    explored = []
    explored.append(start)
    fringe = util.Queue()
    queue_tuple = (start,[])
    fringe.push(queue_tuple)
    while not fringe.isEmpty():
        state, actions = fringe.pop()
        if problem.isGoalState(state):
            return actions
        successor = problem.getSuccessors(state)
        for i in successor:
            coordinates = i[0]
            if not coordinates in explored:
                direction = i[1]
                explored.append(coordinates)
                fringe.push((coordinates, actions+[direction]))
    return actions+[direction]
    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    explored = []
    fringe = util.PriorityQueue()
    fringe.push((start, []),0)
    while not fringe.isEmpty():
        state, action = fringe.pop()
        if problem.isGoalState(state):
            return action
        if state not in explored:
            successor = problem.getSuccessors(state)
            for i in successor:
                coordinates = i[0]
                if not coordinates in explored:
                    direction = i[1]
                    newCost = action+[direction]
                    fringe.push((coordinates, action+[direction]),problem.getCostOfActions(newCost))
        explored.append(state)
    return action+[direction]
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    closeSet = []
    fringe = util.PriorityQueue()
    fringe.push((start, []),nullHeuristic(start, problem))
    cost = 0
    while not fringe.isEmpty():
        state, action = fringe.pop()
        if problem.isGoalState(state):
            return action
        if state not in closeSet:
            successor = problem.getSuccessors(state)
            for i in successor:
                coordinates = i[0]
                if not coordinates in closeSet:
                    direction = i[1]
                    nAction = action+[direction]
                    cost = problem.getCostOfActions(nAction) + heuristic(coordinates, problem)
                    fringe.push((coordinates, nAction), cost)
        closeSet.append(state)
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
