"""
Analysis question.
Change these default values to obtain the specified policies through value iteration.
If any question is not possible, return just the constant NOT_POSSIBLE:
```
return NOT_POSSIBLE
```
"""

NOT_POSSIBLE = None

def question2():
    """
    Changed the answerNoise parameter from 0.2 to 0.0
    in order for the agent to always go to the intended successor
    state when performing an action. This takes away the possibility of
    ending up in an unintended succerssor state when performing an action.
    """

    answerDiscount = 0.9
    answerNoise = 0.0

    return answerDiscount, answerNoise

def question3a():
    """
    Changed the answerNoise parameter from 0.2 to 0.0
    and the answerDiscount parameter from 0.9 to 0.3
    in order to prefer the close exit and risk the cliff.
    """

    answerDiscount = 0.3
    answerNoise = 0.0
    answerLivingReward = 0.0

    return answerDiscount, answerNoise, answerLivingReward

def question3b():
    """
    Changed the answerDiscount parameter from 0.9 to 0.1,
    the answerNoise parameter from 0.2 to 0.1, and the
    answerLivingReward from 0.0 to 0.7 in order to prefer
    the close exit but avoiding the cliff.
    """

    answerDiscount = 0.1
    answerNoise = 0.1
    answerLivingReward = 0.7

    return answerDiscount, answerNoise, answerLivingReward

def question3c():
    """
    Changed the answerNoise parameter from 0.2 to 0.0
    in order to prefer the distant exit and risk the cliff.
    """

    answerDiscount = 0.9
    answerNoise = 0.0
    answerLivingReward = 0.0

    return answerDiscount, answerNoise, answerLivingReward

def question3d():
    """
    Changed the answerNoise parameter from 0.2 to 0.5
    and the answerLivingReward from 0.0 to 1.0 in order to
    prefer the distant exit and avoid the cliff.
    """

    answerDiscount = 0.9
    answerNoise = 0.5
    answerLivingReward = 1.0

    return answerDiscount, answerNoise, answerLivingReward

def question3e():
    """
    Changed the answerNoise parameter from 0.2 to 0.1
    and the answerLivingReward parameter from 0.0 to 100
    in order to avoid both exits and avoid the cliff.
    """

    answerDiscount = 0.9
    answerNoise = 0.1
    answerLivingReward = 100

    return answerDiscount, answerNoise, answerLivingReward

def question6():
    """
    An epsilon and a learning rate does not exist
    for which it is highly likely (greater than 99%)
    that the optimal policy will be learned after 50 iterations.
    Therefore I returned the constant NOT_POSSIBLE.
    """

    return NOT_POSSIBLE

if __name__ == '__main__':
    questions = [
        question2,
        question3a,
        question3b,
        question3c,
        question3d,
        question3e,
        question6,
    ]

    print('Answers to analysis questions:')
    for question in questions:
        response = question()
        print('    Question %-10s:\t%s' % (question.__name__, str(response)))
