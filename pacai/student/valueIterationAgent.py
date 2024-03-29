from pacai.agents.learning.value import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
    A value iteration agent.

    Make sure to read `pacai.agents.learning` before working on this class.

    A `ValueIterationAgent` takes a `pacai.core.mdp.MarkovDecisionProcess` on initialization,
    and runs value iteration for a given number of iterations using the supplied discount factor.

    Some useful mdp methods you will use:
    `pacai.core.mdp.MarkovDecisionProcess.getStates`,
    `pacai.core.mdp.MarkovDecisionProcess.getPossibleActions`,
    `pacai.core.mdp.MarkovDecisionProcess.getTransitionStatesAndProbs`,
    `pacai.core.mdp.MarkovDecisionProcess.getReward`.

    Additional methods to implement:

    `pacai.agents.learning.value.ValueEstimationAgent.getQValue`:
    The q-value of the state action pair (after the indicated number of value iteration passes).
    Note that value iteration does not necessarily create this quantity,
    and you may have to derive it on the fly.

    `pacai.agents.learning.value.ValueEstimationAgent.getPolicy`:
    The policy is the best action in the given state
    according to the values computed by value iteration.
    You may break ties any way you see fit.
    Note that if there are no legal actions, which is the case at the terminal state,
    you should return None.
    """

    def __init__(self, index, mdp, discountRate = 0.9, iters = 100, **kwargs):
        super().__init__(index, **kwargs)

        self.mdp = mdp
        self.discountRate = discountRate
        self.iters = iters
        self.values = {}  # A dictionary which holds the q-values for each state.

        # Compute the values here.
        while self.iters > 0:
            temp_values = self.values.copy()
            all_states = mdp.getStates()
            for state in all_states:
                possible_actions = mdp.getPossibleActions(state)
                possible_qvalues = []
                for action in possible_actions:
                    next_states_info = mdp.getTransitionStatesAndProbs(state, action)
                    qvalue = 0
                    for next_state_info in next_states_info:
                        next_state = next_state_info[0]
                        probability = next_state_info[1]
                        qvalue = qvalue + (probability * (mdp.getReward(state, action, next_state)
                                    + (self.discountRate * temp_values.get(next_state, 0.0))))
                    possible_qvalues.append(qvalue)
                if len(possible_qvalues) != 0:
                    self.values[state] = max(possible_qvalues)
            self.iters = self.iters - 1

    def getValue(self, state):
        """
        Return the value of the state (computed in __init__).
        """

        return self.values.get(state, 0.0)

    def getAction(self, state):
        """
        Returns the policy at the state (no exploration).
        """

        return self.getPolicy(state)

    def getQValue(self, state, action):
        next_states_info = self.mdp.getTransitionStatesAndProbs(state, action)
        qvalue = 0.0
        for next_state_info in next_states_info:
            next_state = next_state_info[0]
            probability = next_state_info[1]
            qvalue = qvalue + (probability * (self.mdp.getReward(state, action, next_state)
                + (self.discountRate * self.getValue(next_state))))
        return qvalue

    def getPolicy(self, state):
        if self.mdp.isTerminal(state):
            return None
        possible_actions = self.mdp.getPossibleActions(state)
        best_policy = ""
        best_qvalue = float("-inf")
        for action in possible_actions:
            qvalue = self.getQValue(state, action)
            if (best_policy == "" and best_qvalue == float("-inf")) or (qvalue >= best_qvalue):
                best_policy = action
                best_qvalue = qvalue
        return best_policy
