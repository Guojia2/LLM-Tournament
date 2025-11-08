import random
from tasks.tasks import Task


class TriviaDuel(Task):

    def __init__(self, questions):
        self.questions = questions

    def init(self, seed=None):
        random.seed(seed)
        state = {
            "round": 0,
            "scores": {0: 0, 1: 0},
            "done": False
        }
        return state

    def observe(self, state, agentId):
        q_idx = state["round"]
        question = self.questions[q_idx]["question"]

        obs = f"=== TRIVIA ROUND {state['round'] + 1} / {len(self.questions)} ===\n\n"
        obs += f"Current Score - You: {state['scores'][agentId]} | Opponent: {state['scores'][1 - agentId]}\n\n"
        obs += f"Question: {question}\n\n"
        obs += "Your answer:"

        return obs

    def step(self, state, actions):
        q_idx = state["round"]
        correct = self.questions[q_idx]["answer"]

        for agentId, action in actions.items():
            if action.strip().lower() == correct.strip().lower():
                state["scores"][agentId] += 1

        state["round"] += 1

        if state["round"] >= len(self.questions):
            state["done"] = True

        return state

    def score(self, state):
        return state["scores"]

    def render(self, state):
        output = f"=== Trivia Duel - Round {state['round']} / {len(self.questions)} ===\n\n"
        output += f"Agent 0 Score: {state['scores'][0]}\n"
        output += f"Agent 1 Score: {state['scores'][1]}\n"

        if state["done"]:
            if state['scores'][0] > state['scores'][1]:
                output += "\nWinner: Agent 0\n"
            elif state['scores'][1] > state['scores'][0]:
                output += "\nWinner: Agent 1\n"
            else:
                output += "\nResult: TIE\n"

        return output