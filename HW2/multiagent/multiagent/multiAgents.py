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


import math
from util import manhattanDistance
from game import Directions
import random
import util

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
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)

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
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        minGhostDist = 9999
        minFoodDist = 0
        ghostDistances = []
        score = successorGameState.getScore()

        for ghost in newGhostStates:
            if ghost.scaredTimer == 0:
                distance = manhattanDistance(newPos, ghost.configuration.pos)
                ghostDistances.append(distance)
                if distance < minGhostDist:
                    minGhostDist = distance
            else:
                score += 10

        # Encourage action that makes the pacman farther from the ghosts
        score += 2 * minGhostDist

        # Game Over:(
        if minGhostDist == 0:
            return -math.inf

        if bool(successorGameState.getNumFood()):
            food = currentGameState.getFood()
            if food[newPos[0]][newPos[1]]:
                minFoodDist = 0
                return score
            else:
                foodDistances = [
                    manhattanDistance(newPos, (x, y))
                    for x in range(food.width)
                    for y in range(food.height)
                    if food[x][y]
                ]
                minFoodDist = min(foodDistances, default=0)
                """ foodDistances = []
                for x in range(food.width):
                    for y in range(food.height):
                        if food[x][y]: 
                            food = manhattanDistance(newPos, (x, y))
                            foodDistances.append(food)
                            if food < minFoodDist:
                                minFoodDist = food """

                # Encourage action that makes the pacman closer to food
                score -= minFoodDist * 2

                # Encourage action that makes the pacman eat food
                if successorGameState.getNumFood() < currentGameState.getNumFood():
                    score += 5

                # Disencourage stop action
                if action == Directions.STOP:
                    score -= 6

                # Encourage action that makes the pacman eat capsules
                if newPos in currentGameState.getCapsules():
                    score += 10
        else:
            # Game is won:)
            return math.inf

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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
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
        util.raiseNotDefined()


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
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
        pacmanActions = gameState.getLegalActions(0)

        v = float('-inf')
        action = None

        for nextPacmanAction in pacmanActions:
            successorValue = self.value(gameState.generateSuccessor(
                0, nextPacmanAction), 1, 0)

            if v < successorValue:
                v = successorValue
                action = nextPacmanAction

        return action

    def value(self, gameState, agentIndex, curDepth):
        if (gameState.isWin() or gameState.isLose() or curDepth == self.depth):
            return self.evaluationFunction(gameState)

        if (agentIndex == 0):  # Our old friend pacman's turn
            return self.max_value(gameState, 0, curDepth)
        else:
            return self.exp_value(gameState, agentIndex, curDepth)

    def max_value(self, gameState, agentIndex, curDepth):
        v = float('-inf')
        # Agent is pacman which means agentIndex is 0, no need to check for next depth
        for action in gameState.getLegalActions(agentIndex):
            v = max(v, self.value(gameState.generateSuccessor(
                    agentIndex, action), agentIndex + 1, curDepth))

        return v

    def exp_value(self, gameState, agentIndex, curDepth):
        v = 0
        for action in gameState.getLegalActions(agentIndex):
            if (agentIndex == gameState.getNumAgents() - 1):  # Continue with the next depth
                v += self.value(gameState.generateSuccessor(
                    agentIndex, action), 0, curDepth + 1)
            else:
                v += self.value(gameState.generateSuccessor(
                    agentIndex, action), agentIndex + 1, curDepth)
        return v / len(gameState.getLegalActions(agentIndex))


def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: In this evaluation the pacman is punished or rewarded based on some parameters of the current state.
    Score is evaluated based on current game score and the pacman is penalized whenever it gets closer to a non-scared
    ghost, it gets away from the foods and when the food count is higher. On the other hand, the pacman is rewarded
    whenever it gets closer to a frozen ghost that encourages it to eat the ghost. This evaluation function has an
    average of 1150.3 points and gets 6/6 from q5.
    """
    "*** YOUR CODE HERE ***"
    curPos = currentGameState.getPacmanPosition()
    curFood = currentGameState.getFood()
    curGhostStates = currentGameState.getGhostStates()
    curScaredGhostTimes = [
        ghostState.scaredTimer for ghostState in curGhostStates]

    foodsAt = curFood.asList()
    foodsLeft = currentGameState.getNumFood()

    foodDistanceList = [manhattanDistance(curPos, food)
                        for food in foodsAt]
    minDistanceFood = min(foodDistanceList) if len(
        foodDistanceList) > 0 else 1

    ghostDistanceList = [(i, manhattanDistance(
        curPos, ghostState.getPosition())) for i, ghostState in enumerate(curGhostStates)]

    ghostDistance = min(ghostDistanceList) if len(ghostDistanceList) > 0 else 0

    ghostPenalty = - \
        (2 - ghostDistance[1]) if not curScaredGhostTimes[ghostDistance[0]
                                                          ] and ghostDistance[1] <= 2 else 0
    frozenGhostReward = 0
    for frozen in curScaredGhostTimes:
        frozenGhostAt = curGhostStates[curScaredGhostTimes.index(
            frozen)].getPosition()
        distanceToFrozen = manhattanDistance(curPos, frozenGhostAt)
        if (frozen > 0 and distanceToFrozen < 5):
            frozenGhostReward += (5 - distanceToFrozen)

    foodPenalty = -1 * minDistanceFood
    eatPenalty = -2.5 * foodsLeft

    return currentGameState.getScore() + foodPenalty + ghostPenalty + frozenGhostReward + eatPenalty


# Abbreviation
better = betterEvaluationFunction
