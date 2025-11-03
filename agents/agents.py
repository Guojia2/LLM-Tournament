class Agent:
    def __init__(self, name, model=None, model_config=None):
        self.name = name
        self.model = model
        self.model_config = model_config or {}

    def act(self, observation):
        if self.model == "dummy":
            return "dummy_action"
        # Call LLM. Can be API, can be local model.
        return self._call_llm(observation)

    def _call_llm(self, observation):
        # Placeholder for actual LLM calls for now.
        return "placeholder"