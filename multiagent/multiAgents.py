# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        score = float(0)
        currFood = currentGameState.getFood().asList()
        x, y = newPos
        for m in range(len(newGhostStates)):
            a, b = newGhostStates[m].getPosition()
            movesAway = abs(x - a) + abs(y - b)
            #food is good
            if newPos in currFood:
                score += 1
            # run away from ghost
            if movesAway < 2:
                score -= 1
            # get higher score if closer to food 
            distanceToFood = []
            for c, d in currFood:
                dis = abs(x-c)
                distanceToFood.append(dis)
            score -= 0.1*min(distanceToFood)
            
            
        return score

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        legal = gameState.getLegalActions(0)
        successors = [gameState.generateSuccessor(0, action) for action in legal]
        maxValue = -float('inf') # smallest float
        goalIndex = 0
        for x in range(len(successors)):
            actionValue = self.value(successors[x], 1, 0)
            if actionValue > maxValue:
                maxValue = actionValue
                goalIndex = x
        return legal[goalIndex]

    def maxValue(self, gameState, agentIndex, depthCurr):
        rv = -float('inf')
        legal = gameState.getLegalActions(agentIndex)
        successors = [gameState.generateSuccessor(0, action) for action in legal]
        for successor in successors:
            rv = max(rv, self.value(successor, 1, depthCurr))
        return rv
    
    def minValue(self, gameState, agentIndex, depthCurr):
        rv = float('inf')
        legal = gameState.getLegalActions(agentIndex)
        successors = [gameState.generateSuccessor(agentIndex, action) for action in legal]
        for successor in successors:
                if agentIndex + 1 == gameState.getNumAgents():
                    rv = min(rv, self.value(successor, 0, depthCurr+1))
                else:
                    rv = min(rv, self.value(successor, agentIndex+1, depthCurr))
        return rv
    
    def value(self, gameState, agentIndex, depthCurr):
        if depthCurr == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if agentIndex == 0:
            return self.maxValue(gameState, agentIndex, depthCurr)
        if agentIndex > 0:
            return self.minValue(gameState, agentIndex, depthCurr)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha = -float('inf')
        beta = float('inf')
        maxValue = -float('inf')
        legal = gameState.getLegalActions(0)
        successors = [gameState.generateSuccessor(0, action) for action in legal]
        for i in range(len(successors)):
            actionValue = self.value(successors[i], 1, 0, alpha, beta)
            if actionValue > maxValue:
                maxValue = actionValue
                goalIndex = i
                alpha = actionValue
        return legal[goalIndex]

    def minValue(self, gameState, agentIndex, depthCurr, alpha, beta):
        returnValue = float('inf')
        legal = gameState.getLegalActions(agentIndex)
        for action in legal:
            successor = gameState.generateSuccessor(agentIndex, action)
            if agentIndex + 1 == gameState.getNumAgents():
                returnValue = min(returnValue, self.value(successor, 0, depthCurr + 1, alpha, beta))
            else :
                returnValue = min(returnValue, self.value(successor, agentIndex + 1, depthCurr, alpha, beta))
            if returnValue < alpha:
                return returnValue
            beta = min(returnValue, beta)
        return returnValue
    
    def maxValue(self, gameState, agentIndex, depthCurr, alpha, beta):
        returnValue = -float('inf')
        legal = gameState.getLegalActions(agentIndex)
        for action in legal:
            successor = gameState.generateSuccessor(agentIndex, action)
            returnValue = max(returnValue, self.value(successor, 1, depthCurr, alpha, beta))
            if returnValue > beta:
                return returnValue  
            alpha = max(alpha, returnValue)
        return returnValue
    
    def value(self, gameState, agentIndex, depthCurr, alpha, beta):
        if depthCurr == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if agentIndex == 0:
            return self.maxValue(gameState, agentIndex, depthCurr, alpha, beta)
        if agentIndex > 0:
            return self.minValue(gameState, agentIndex, depthCurr, alpha, beta)
    
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        maxValue = - float('inf')
        goalIndex = 0
        legal = gameState.getLegalActions(0)
        successors = [gameState.generateSuccessor(0, action) for action in legal]
        for i in range(len(successors)):
            actionValue = self.value(successors[i], 1, 0)
            if actionValue > maxValue:
                maxValue = actionValue
                goalIndex = i
        return legal[goalIndex]

    def minValue(self, gameState, agentIndex, depthCurr):
        returnValue = float(0)
        legal = gameState.getLegalActions(agentIndex)
        successors = [gameState.generateSuccessor(agentIndex, action) for action in legal]
        for successor in successors:
            if agentIndex + 1 == gameState.getNumAgents():
                returnValue += self.value(successor, 0, depthCurr + 1)
            else:
                returnValue += self.value(successor, agentIndex + 1, depthCurr)
        return returnValue/len(successors)
    def maxValue(self, gameState, agentIndex, depthCurr):
        returnValue = - float('inf')
        legal = gameState.getLegalActions(agentIndex)
        successors = [gameState.generateSuccessor(agentIndex, action) for action in legal]
        for successor in successors:
            returnValue = max(returnValue, self.value(successor, 1, depthCurr))
        return returnValue
    def value(self, gameState, agentIndex, depthCurr):
        if depthCurr == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if agentIndex == 0:
            return self.maxValue(gameState, agentIndex, depthCurr)
        if agentIndex > 0:
            return self.minValue(gameState, agentIndex, depthCurr)
        

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    
    Pos = currentGameState.getPacmanPosition()
    Food = currentGameState.getFood().asList()
    GhostStates = currentGameState.getGhostStates()
    ScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]
    FOOD_WEIGHT = 10.0
    SCARED_GHOST_WEIGHT = 100.0
    GHOST_WETGHT = -10.0
    
    def evalHelper(currentGameState, Pos):
        x, y = Pos
        score = currentGameState.getScore() 
        for i in range(len(GhostStates)):
            a, b = GhostStates[i].getPosition()
            ghostDis = abs(x - a) + abs (y - b)
            if ghostDis > 0:
                if ScaredTimes[i]:
                    score += SCARED_GHOST_WEIGHT / ghostDis
                else:
                    score += GHOST_WETGHT / ghostDis
            else:
                return -float('inf')
        foodDistance = []
        for c, d in Food:
            foodDis = abs(x - c) + abs (y - d)
            foodDistance.append(foodDis)
        if len(foodDistance) > 0:
            score += FOOD_WEIGHT / min(foodDistance)
        else:
            score += FOOD_WEIGHT
        
            
        return score
    return evalHelper(currentGameState, Pos)
# Abbreviation
better = betterEvaluationFunction
