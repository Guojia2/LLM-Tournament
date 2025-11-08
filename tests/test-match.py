from engine.orchestration_engine import run_match
from tasks.negotiation_game import NegotiationGame
from tasks.trivia_duel import TriviaDuel
from agents.agents import Agent

questions = [
    {"question": "What is 2+2?", "answer": "4"},
    {"question": "What is the capital of France?", "answer": "Paris"},
    {"question": "Who wrote Romeo and Juliet?", "answer": "Shakespeare"}
]

task = TriviaDuel(questions)
agent1 = Agent("Claude", model="claude-3-5-sonnet-20241022")
agent2 = Agent("Gemini", model="gemini-pro")

result = run_match(task, [agent1, agent2], seed=42, log_dir="logs")
# Creates logs/20241108_143022_TriviaDuel_Claude_vs_Gemini.json
# Creates logs/20241108_143022_TriviaDuel_Claude_vs_Gemini_readable.txt

task2 = NegotiationGame()
result2 = run_match(task2, [agent1, agent2], seed=42, log_dir="logs")