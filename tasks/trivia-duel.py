import random



class TriviaTask:
    def __init__(self, questions):
        self.questions = questions

    def init(self, seed=None):
        random.seed(seed)
        self.state = {"round": 0, "scores": {0: 0, 1: 0}}
        return self.state

    def observe(self, state, agentId):
        q_idx = state["round"]
        return self.questions[q_idx]["question"]

    def step(self, state, actions):
        q_idx = state["round"]
        correct = self.questions[q_idx]["answer"]

        for agentId, action in actions.items():
            if action == correct:
                state["scores"][agentId] += 1

        state["round"] += 1
        return state

    def score(self, state):
        return state["scores"]
