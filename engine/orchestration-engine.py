


def run_match(task, agents, seed=42):
    state = task.init(seed)
    while state["round"] < len(task.questions):
        actions = {}
        for agentId, agent in enumerate(agents):
            obs = task.observe(state, agentId)
            action = agent.act(obs)
            actions[agentId] = action
        state = task.step(state, actions)

    return task.score(state)
