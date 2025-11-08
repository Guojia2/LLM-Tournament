import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tasks.tasks import Task
from tasks.trivia_duel import TriviaDuel
from tasks.negotiation_game import NegotiationGame
from agents.agents import Agent
from engine.orchestration_engine import run_match


def test_task_interface():
    print("\n=== Task Interface ===")
    
    questions = [
        {"question": "What is 2+2?", "answer": "4"},
        {"question": "What is the capital of France?", "answer": "Paris"}
    ]
    trivia = TriviaDuel(questions)
    
    assert isinstance(trivia, Task)
    assert hasattr(trivia, 'init')
    assert hasattr(trivia, 'observe')
    assert hasattr(trivia, 'step')
    assert hasattr(trivia, 'score')
    
    print("TriviaDuel looks good")
    
    negotiation = NegotiationGame(items_per_agent=3, max_rounds=5)
    assert isinstance(negotiation, Task)
    print("NegotiationGame looks good")
    
    return True


def test_trivia_mechanics():
    print("\n=== TriviaDuel Mechanics ===")
    
    questions = [
        {"question": "What is 2+2?", "answer": "4"},
        {"question": "Capital of France?", "answer": "Paris"}
    ]
    task = TriviaDuel(questions)
    
    state = task.init(seed=42)
    assert state["round"] == 0
    assert state["scores"] == {0: 0, 1: 0}
    assert state["done"] == False
    print("init works")
    
    obs = task.observe(state, 0)
    assert "What is 2+2?" in obs
    print("observe works")
    
    actions = {0: "4", 1: "5"}
    state = task.step(state, actions)
    assert state["scores"][0] == 1
    assert state["scores"][1] == 0
    assert state["round"] == 1
    print("step and scoring work")
    
    state = task.step(state, {0: "Paris", 1: "London"})
    assert state["done"] == True
    print("game completion works")
    
    scores = task.score(state)
    assert scores[0] == 2
    assert scores[1] == 0
    print("final scoring works")
    
    return True


def test_negotiation_mechanics():
    print("\n=== NegotiationGame Mechanics ===")
    
    task = NegotiationGame(items_per_agent=3, max_rounds=5, hidden_inventory=False)
    
    state = task.init(seed=42)
    assert state["round"] == 0
    assert len(state["inventories"][0]) == 3
    assert len(state["inventories"][1]) == 3
    assert state["done"] == False
    print("init works")
    
    obs = task.observe(state, 0)
    assert "YOUR INVENTORY:" in obs
    assert "OPPONENT'S INVENTORY:" in obs
    print("observe works")
    
    actions = {
        0: "Hello, shall we trade?",
        1: "Sure, what do you propose?"
    }
    state = task.step(state, actions)
    assert len(state["conversation"]) == 2
    assert state["round"] == 1
    print("conversation tracking works")
    
    agent0_items = state["inventories"][0]
    agent1_items = state["inventories"][1]
    actions = {
        0: f"PROPOSE: I give {agent0_items[0]} for your {agent1_items[0]}",
        1: "Let me think..."
    }
    state = task.step(state, actions)
    assert state["current_proposal"] is not None
    print("proposal parsing works")
    
    actions = {0: "Waiting...", 1: "ACCEPT"}
    state = task.step(state, actions)
    assert state["deal_completed"] == True
    assert state["done"] == True
    print("deal acceptance works")
    
    scores = task.score(state)
    assert "gain" in scores[0]
    assert "initial_value" in scores[0]
    print("utility scoring works")
    
    return True


def test_agent():
    print("\n=== Agent ===")
    
    agent = Agent("TestAgent", model="dummy")
    obs = "What is 2+2?"
    action = agent.act(obs)
    assert action is not None
    print(f"agent returns: '{action}'")
    
    return True


def test_orchestration():
    print("\n=== Orchestration Engine ===")
    
    questions = [
        {"question": "What is 2+2?", "answer": "4"},
        {"question": "Capital of France?", "answer": "Paris"}
    ]
    task = TriviaDuel(questions)
    
    # mock agents with predetermined answers
    class MockAgent(Agent):
        def __init__(self, name, answers):
            super().__init__(name, model="mock")
            self.answers = answers
            self.call_count = 0
        
        def act(self, observation):
            answer = self.answers[self.call_count % len(self.answers)]
            self.call_count += 1
            return answer
    
    agent0 = MockAgent("SmartAgent", ["4", "Paris"])
    agent1 = MockAgent("DumbAgent", ["5", "London"])
    
    result = run_match(task, [agent0, agent1], seed=42)
    
    assert "scores" in result
    assert "transcript" in result
    assert "final_state" in result
    print("result structure is correct")
    
    assert result["scores"][0] == 2
    assert result["scores"][1] == 0
    print("scores are correct")
    
    assert len(result["transcript"]) > 0
    assert "observation" in result["transcript"][0]
    assert "action" in result["transcript"][0]
    print("transcript looks good")
    
    # test negotiation
    print("\nTesting negotiation match...")
    task = NegotiationGame(items_per_agent=2, max_rounds=3)
    
    agent0 = MockAgent("Trader1", ["Hello!", "PROPOSE: I give Apple for your Carrot", "Waiting..."])
    agent1 = MockAgent("Trader2", ["Hi!", "Interesting...", "ACCEPT"])
    
    result = run_match(task, [agent0, agent1], seed=123)
    
    assert result["scores"][0]["deal_completed"] == True
    print("negotiation match completed")
    
    return True


def run_all():
    print("=" * 60)
    print("MILESTONE 1: Agent/Task API + Runner Logic")
    print("=" * 60)
    
    tests = [
        ("Task Interface", test_task_interface),
        ("TriviaDuel Mechanics", test_trivia_mechanics),
        ("NegotiationGame Mechanics", test_negotiation_mechanics),
        ("Agent", test_agent),
        ("Orchestration Engine", test_orchestration),
    ]
    
    passed = 0
    failed = 0
    
    for name, func in tests:
        try:
            func()
            passed += 1
            print(f"\nPASSED: {name}")
        except Exception as e:
            failed += 1
            print(f"\nFAILED: {name}")
            print(f"Error: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed == 0:
        print("\nAll tests passed! Thank god..")

    else:
        print("\nSome tests failed, fix issues above")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)