# judges/judge.py


"""
This will probably not be used for the negotiation or trivia duel tasks, as they are self-scoring.
I thought we might use this for the coding battle, but I haven't decided how to proceed with that task.
It may be useful for some future tasks, though.

"""
class Judge:
    def evaluate(self, state, task_type):
        """
        Returns scores for agents based on task state
        """
        pass

class RuleBasedJudge(Judge):
    # For tasks with clear winners. May not be useful, as those may all be self-scoring
    pass

class LLMJudge(Judge):
    # For subjective tasks (code quality, creative writing, persuasion).
    pass