def run_match(task, agents, seed=42):
    state = task.init(seed)
    transcript = []

    while not state.get("done", False):
        actions = {}
        for agentId, agent in enumerate(agents):
            obs = task.observe(state, agentId)
            action = agent.act(obs)
            actions[agentId] = action
            transcript.append({
                "round": state.get("round", 0),
                "agent": agentId,
                "observation": obs,
                "action": action
            })
        state = task.step(state, actions)

    scores = task.score(state)
    return {"scores": scores, "transcript": transcript, "final_state": state}