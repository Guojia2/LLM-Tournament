class Agent:
    def __init__(self, name, model=None):
        self.name = name
        self.model = model  # could be OpenAI API, local model, or dummy

    def act(self, observation):
        """Return an action given the observation."""
        # For now, return something random/dummy
        return "dummy_action"

