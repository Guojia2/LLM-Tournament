import json
from datetime import datetime
from pathlib import Path


def run_match(task, agents, seed=42, log_dir = "logs"):
    """
     Run a match between agents and log the results.

     Args:
         task: Task instance
         agents: List of Agent instances
         seed: Random seed for reproducibility
         log_dir: Directory to save match logs

     """
    # create log directory if it doesn't exist
    Path(log_dir).mkdir(exist_ok=True)

    # generate match id
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    task_name = task.__class__.__name__
    agent_names = "_vs_".join([agent.name for agent in agents])
    match_id = f"{timestamp}_{task_name}_{agent_names}"

    # initialize match
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

    # prepare result
    result = {
        "match_id": match_id,
        "timestamp": timestamp,
        "task": task_name,
        "agents": [{"id": i, "name": agent.name, "model": agent.model}
                   for i, agent in enumerate(agents)],
        "seed": seed,
        "scores": scores,
        "transcript": transcript,
        "final_state": state
    }
    # save to json
    log_path = Path(log_dir) / f"{match_id}.json"
    with open(log_path, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"Match logged to: {log_path}")
    # also save human-readable version
    readable_path = Path(log_dir) / f"{match_id}_readable.txt"
    with open(readable_path, 'w') as f:
        _write_readable_log(f, result, task)

    print(f"Readable log: {readable_path}")

    return result


def _write_readable_log(f, result, task):
    """Write a human-readable version of the match log."""
    f.write("=" * 80 + "\n")
    f.write(f"MATCH: {result['match_id']}\n")
    f.write("=" * 80 + "\n\n")

    f.write(f"Task: {result['task']}\n")
    f.write(f"Timestamp: {result['timestamp']}\n")
    f.write(f"Seed: {result['seed']}\n\n")

    f.write("Agents:\n")
    for agent in result['agents']:
        f.write(f"  [{agent['id']}] {agent['name']} ({agent['model']})\n")
    f.write("\n")

    f.write("=" * 80 + "\n")
    f.write("TRANSCRIPT\n")
    f.write("=" * 80 + "\n\n")

    for entry in result['transcript']:
        f.write(f"--- Round {entry['round']} | Agent {entry['agent_id']} ({entry['agent_name']}) ---\n")
        f.write(f"\nObservation:\n{entry['observation']}\n")
        f.write(f"\nAction:\n{entry['action']}\n")
        f.write("\n" + "-" * 80 + "\n\n")

    f.write("=" * 80 + "\n")
    f.write("FINAL SCORES\n")
    f.write("=" * 80 + "\n\n")

    scores = result['scores']
    for agent_id, score in scores.items():
        agent_name = result['agents'][agent_id]['name']
        f.write(f"Agent {agent_id} ({agent_name}):\n")
        if isinstance(score, dict):
            for key, value in score.items():
                f.write(f"  {key}: {value}\n")
        else:
            f.write(f"  Score: {score}\n")
        f.write("\n")

    f.write("=" * 80 + "\n")
    f.write("FINAL STATE\n")
    f.write("=" * 80 + "\n\n")
    f.write(task.render(result['final_state']))