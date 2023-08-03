import random

from pacai.agents.base import BaseAgent
from pacai.agents.search.multiagent import MultiAgentSearchAgent
from pacai.core.distance import manhattan

class ReflexAgent(BaseAgent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.
    You are welcome to change it in any way you see fit,
    so long as you don't touch the method headers.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        `ReflexAgent.getAction` chooses among the best options according to the evaluation function.

        Just like in the previous project, this method takes a
        `pacai.core.gamestate.AbstractGameState` and returns some value from
        `pacai.core.directions.Directions`.
        """

        # Collect legal moves.
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions.
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best.

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current `pacai.bin.pacman.PacmanGameState`
        and an action, and returns a number, where higher numbers are better.
        Make sure to understand the range of different values before you combine them
        in your evaluation function.
        """

        successorGameState = currentGameState.generatePacmanSuccessor(action)

        # Useful information you can extract.
        # newPosition = successorGameState.getPacmanPosition()
        # oldFood = currentGameState.getFood()
        # newGhostStates = successorGameState.getGhostStates()
        # newScaredTimes = [ghostState.getScaredTimer() for ghostState in newGhostStates]

        # *** Your Code Here ***
        # Getting the food/capsules available before and after taking the action
        oldFood = currentGameState.getFood().asList()
        newFood = successorGameState.getFood().asList()
        oldCapsules = currentGameState.getCapsules()
        newCapsules = successorGameState.getCapsules()

        # Checking if PacMan ate a food or not after taking the action
        ate_food_points = 0
        if len(oldFood) != len(newFood):
            ate_food_points = 1000

        # Checking if Pacman ate a capsule or not after taking the action
        ate_capsule_points = 0
        if len(oldCapsules) != len(newCapsules):
            ate_capsule_points = 200

        # Getting the closest and furthest food pellet after taking the action
        newPosition = successorGameState.getPacmanPosition()
        closest_pellet_distance = -1
        furthest_pellet_distance = -1
        for food in newFood:
            distance = manhattan(newPosition, food)
            if closest_pellet_distance == -1 or closest_pellet_distance > distance:
                closest_pellet_distance = distance
            if furthest_pellet_distance == -1 or distance > furthest_pellet_distance:
                furthest_pellet_distance = distance

        # Calculating the number of ghosts that are extremely close
        close_ghosts_counter = 0
        ghost_positions = successorGameState.getGhostPositions()
        for ghostPosition in ghost_positions:
            distance = manhattan(newPosition, ghostPosition)
            if distance <= 1:
                close_ghosts_counter = close_ghosts_counter + 1

        return (successorGameState.getScore() - closest_pellet_distance
            - furthest_pellet_distance - (close_ghosts_counter * 10000)
            + ate_food_points + ate_capsule_points)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    A minimax agent.

    Here are some method calls that might be useful when implementing minimax.

    `pacai.core.gamestate.AbstractGameState.getNumAgents()`:
    Get the total number of agents in the game

    `pacai.core.gamestate.AbstractGameState.getLegalActions`:
    Returns a list of legal actions for an agent.
    Pacman is always at index 0, and ghosts are >= 1.

    `pacai.core.gamestate.AbstractGameState.generateSuccessor`:
    Get the successor game state after an agent takes an action.

    `pacai.core.directions.Directions.STOP`:
    The stop direction, which is always legal, but you may not want to include in your search.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):
        def value(agent, depth, s):
            if s.isLose() or s.isWin() or depth == self.getTreeDepth():
                return self.getEvaluationFunction()(s)
            if agent == 0:
                return maxValue(agent, depth, s)
            else:
                return minValue(agent, depth, s)

        def maxValue(agent, depth, s):
            max = float('-inf')
            for action in s.getLegalActions(0):
                temp_value = value(1, depth, s.generateSuccessor(0, action))
                if temp_value > max:
                    max = temp_value
            return max

        def minValue(agent, depth, s):
            nextAgent = agent + 1
            if nextAgent == s.getNumAgents():
                nextAgent = 0
                depth = depth + 1

            min = float('inf')
            for action in s.getLegalActions(agent):
                temp_value = value(nextAgent, depth, s.generateSuccessor(agent, action))
                if temp_value < min:
                    min = temp_value
            return min

        # Collect legal moves.
        legalMoves = gameState.getLegalActions(0)

        # Choose one of the best actions.
        scores = [value(1, 0, gameState.generateSuccessor(0, action)) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best.

        return legalMoves[chosenIndex]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    A minimax agent with alpha-beta pruning.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):
        def value(agent, depth, s, alpha, beta):
            if s.isLose() or s.isWin() or depth == self.getTreeDepth():
                return self.getEvaluationFunction()(s)
            if agent == 0:
                return maxValue(agent, depth, s, alpha, beta)
            else:
                return minValue(agent, depth, s, alpha, beta)

        def maxValue(agent, depth, s, alpha, beta):
            max_val = float('-inf')
            for action in s.getLegalActions(0):
                temp_value = value(1, depth, s.generateSuccessor(0, action), alpha, beta)
                if temp_value > max_val:
                    max_val = temp_value
                alpha = max(alpha, temp_value)
                if beta <= alpha:
                    break
            return max_val

        def minValue(agent, depth, s, alpha, beta):
            nextAgent = agent + 1
            if nextAgent == s.getNumAgents():
                nextAgent = 0
                depth = depth + 1

            min_val = float('inf')
            for action in s.getLegalActions(agent):
                temp_value = value(nextAgent, depth,
                                s.generateSuccessor(agent, action), alpha, beta)
                if temp_value < min_val:
                    min_val = temp_value
                beta = min(beta, temp_value)
                if beta <= alpha:
                    break
            return min_val

        # Collect legal moves.
        legalMoves = gameState.getLegalActions(0)

        # Choose one of the best actions.
        alpha = float('-inf')
        beta = float('inf')
        scores = [value(1, 0, gameState.generateSuccessor(0, action), alpha, beta)
                  for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best.

        return legalMoves[chosenIndex]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    An expectimax agent.

    All ghosts should be modeled as choosing uniformly at random from their legal moves.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the expectimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):
        def value(agent, depth, s):
            if s.isLose() or s.isWin() or depth == self.getTreeDepth():
                return self.getEvaluationFunction()(s)
            if agent == 0:
                return maxValue(agent, depth, s)
            else:
                return minValue(agent, depth, s)

        def maxValue(agent, depth, s):
            max = float('-inf')
            for action in s.getLegalActions(0):
                temp_value = value(1, depth, s.generateSuccessor(0, action))
                if temp_value > max:
                    max = temp_value
            return max

        def minValue(agent, depth, s):
            nextAgent = agent + 1
            if nextAgent == s.getNumAgents():
                nextAgent = 0
                depth = depth + 1

            sum = 0
            for action in s.getLegalActions(agent):
                temp_value = value(nextAgent, depth, s.generateSuccessor(agent, action))
                sum = sum + temp_value
            return sum / len(s.getLegalActions(agent))

        # Collect legal moves.
        legalMoves = gameState.getLegalActions(0)

        # Choose one of the best actions.
        scores = [value(1, 0, gameState.generateSuccessor(0, action)) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best.

        return legalMoves[chosenIndex]

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable evaluation function.

    DESCRIPTION: <write something here so we know what you did>
    """
    # Getting the food/capsules available
    food_available = currentGameState.getFood().asList()
    capsules_available = len(currentGameState.getCapsules())

    # Getting the closest food pellet
    position = currentGameState.getPacmanPosition()
    closest_pellet_distance = -1
    for food in food_available:
        distance = manhattan(position, food)
        if closest_pellet_distance == -1 or closest_pellet_distance > distance:
            closest_pellet_distance = distance

    # Calculating the number of ghosts that are extremely close
    # and the sum of all the distances from Pacman to the ghosts
    close_ghosts_counter = 0
    ghost_positions = currentGameState.getGhostPositions()
    total_ghost_distance = 1
    for ghostPosition in ghost_positions:
        distance = manhattan(position, ghostPosition)
        total_ghost_distance = total_ghost_distance + distance
        if distance <= 1:
            close_ghosts_counter = close_ghosts_counter + 1

    # Giving a big bonus point if state is a winning state
    won_state_bonus = 0
    if currentGameState.isWin():
        won_state_bonus = 100000000

    return (currentGameState.getScore() + (1 / closest_pellet_distance)
        - (1 / total_ghost_distance) - (close_ghosts_counter * 10000)
        - capsules_available + won_state_bonus)

class ContestAgent(MultiAgentSearchAgent):
    """
    Your agent for the mini-contest.

    You can use any method you want and search to any depth you want.
    Just remember that the mini-contest is timed, so you have to trade off speed and computation.

    Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
    just make a beeline straight towards Pacman (or away if they're scared!)

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
